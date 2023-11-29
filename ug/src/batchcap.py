# https://raw.githubusercontent.com/SuperArbor/batchcap/main/BatchCap.py
from enum import Enum
import os, sys, tempfile
import json, re
import psutil
import argparse
from subprocess import Popen, PIPE
from loguru import logger
from Tree import *
from traceback import format_exc
from tqdm import tqdm
from datetime import datetime, timedelta
from fractions import Fraction

NL = '\n'
MIN_FONTSIZE = 1
MAX_FONTSIZE = 999
MAX_LOG_LENGTH = 2048           # Maximum length of an entry of logging
MEMORY_PARA = 6                 # Coefficient to decide the capture method to call
MIN_FFMPEG_MAIN_VERSION = 4
MAX_COMMAND_LENGTH = 20000      # Maximum length of the command for the system to run

if os.name == 'nt':
    FONTFILE = 'C:/Windows/Fonts/arial.ttf'
else:
    FONTFILE = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'

def debugger_is_active() -> bool:
    """Return if the debugger is currently active"""
    gettrace = getattr(sys, 'gettrace', lambda : None) 
    return gettrace() is not None

class AsyncError(Exception):
    def __init__(self, cmd:str, out, err) -> None:
        self.cmd = cmd
        self.out = out
        self.err = err
    def __repr__(self) -> str:
        return self.cmd + ' error'

class CaptureResult(Enum):
    SUCCEEDED = 0
    PROBE_FAILED = -1
    CAPTURE_ERROR_OCCURED = 1
    CAPTURE_FAILED = -2
    
    def __str__(self) -> str:
        return self.name

def run_async(args, stdin=PIPE, stdout=PIPE, stderr=PIPE, multiple=False):
    '''Call the command(s) in another process.
    multiple: whether there are more than one commands in cmds to be chained by pipes.
    '''
    if multiple:
        process = None
        for cmd in args:
            if process:
                process = Popen(cmd, stdin=process.stdout, stdout=stdout, stderr=stderr)
            else:
                process = Popen(cmd, stdin=stdin, stdout=stdout, stderr=stderr)
    else:
        process = Popen(args, stdin=stdin, stdout=stdout, stderr=stderr)
    
    out, err = process.communicate()
    out, err = out.decode('utf-8'), err.decode('utf-8')
    retcode = process.poll()
    if retcode != 0:
        cmd = 'unknown'
        if isinstance(args, list):
            if len(args) > 0:
                cmd = args[0]
        elif isinstance(args, str):
            cmd = args
        raise AsyncError(cmd, out, err)
    return out, err

def probe_file(file:str):
    '''Returns basic information of a video.'''
    if not os.path.isfile(file):
        raise FileNotFoundError(f"{file}")
    args = ['ffprobe', '-show_format', '-show_streams', '-loglevel', 'error', '-of', 'json', file]
    
    out, err = run_async(args)
    if err:
        logger.error(f'Error occured during probing {file}:{NL}{suppress_log(err)}')
        
    probe = json.loads(out)
    video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
    try:
        avg_frame_rate = Fraction(video_info['avg_frame_rate'])
        frame_rate = float(avg_frame_rate.numerator / avg_frame_rate.denominator)
    except ZeroDivisionError:
        r_frame_rate = Fraction(video_info['r_frame_rate'])
        frame_rate = float(r_frame_rate.numerator / r_frame_rate.denominator)
        
    width, height = int(video_info['width']), int(video_info['height'])
    duration = float(probe['format']['duration'])
    size = float(probe['format']['size'])
    return {'avg_frame_rate': frame_rate, 'width': width, 'height': height, 'duration': duration, 'size': size}

def suppress_log(message:str, max_length=MAX_LOG_LENGTH):
    '''Suppress logging output in case the content is too long.'''
    if len(message) <= max_length:
        return message
    else:
        return message[:max_length] + '...'

def escape_chars(text, chars, escape='\\'):
    """Helper function to escape uncomfortable characters."""
    text = str(text)
    chars = list(set(chars))
    if '\\' in chars:
        chars.remove('\\')
        chars.insert(0, '\\')
    for ch in chars:
        text = text.replace(ch, escape + ch)
    return text

def capture_file_once_cmd(file:str, args, capture_info:dict):
    '''Get the command to capture a video according to arguments.
    
    It is done by generating a command and use subprocess to run it. 
    The command will be something like:
    
    ['ffmpeg', 
        '-ss', '10.0', '-i', 'video.mkv', 
        '-ss', '133.86', '-i', 'video.mkv', 
        '-filter_complex', 
            '[0:v:0]scale=-1:270[a0];[a0]drawtext=fontcolor=yellow:fontfile=C\\\\:/Windows/Fonts/arial.ttf:fontsize=20:text=0\\\\:00\\\\:10:x=text_h:y=text_h[v0];
            [1:v:0]scale=-1:270[a1];[a1]drawtext=fontcolor=yellow:fontfile=C\\\\:/Windows/Fonts/arial.ttf:fontsize=20:text=0\\\\:02\\\\:13.860000:x=text_h:y=text_h[v1];
            [v0][v1]xstack=inputs=2:layout=0_0.0|270_0.0[c]', 
        '-map', '[c]', 
        '-frames:v', '1', 
        '-loglevel', 'error', 
        'video_cap.png', 
        '-y']
    
    Some of the arguments, like the 'text=0\\\\:00\\\\:10' is calculated in the code.
    
    Another way to do this is:
    
    ['ffmpeg',
        '-i', 'video.mkv', 
        '-filter_complex', 
            '[0]select=not(mod(n - 0\, 308.0)) * not(lt(n\, 0))[s0];[s0]scale=-1:270[s1];[s1]tile=5x4[s2]',
        '-map', [s2],
        '-frames:v', '1', 
        '-loglevel', 'error', 
        'video_cap.png',
        '-y']
    
    Though looking much easier, the second way is computationally expensive.
    '''
    output_name = capture_info['output_name']
    seek = capture_info['seek']
    interval = capture_info['interval']
    width, height = capture_info['width'], capture_info['height']
    c, r = capture_info['columns'], capture_info['rows']
    pad = capture_info['pad']
    fontsize = capture_info['fontsize']
    
    # Generating command
    cmd = ['ffmpeg']
    for i in range(c * r):
        cmd.extend(['-ss', f'{seek + i*interval}', '-i', file])
    
    cmd.append('-filter_complex')
    if args.timestamp:
        fontfile = escape_chars(FONTFILE, r"\' =:", r'\\')
        def get_timestamp(t):
            h, m, s = str(timedelta(seconds=t)).split(':')
            t = f'{h}:{m}:{float(s):.3f}'
            return escape_chars(t, r"\'=:", r'\\')
        cmd.append (
                    ''.join([f'[{i}:v:0]scale=-1:{args.height}[a{i}];\
                                [a{i}]drawtext=fontcolor={args.fontcolor}:fontfile={fontfile}:fontsize={fontsize}:text={get_timestamp(seek + i*interval)}:x=text_h:y=text_h[b{i}];\
                                [b{i}]format=rgba[c{i}];[c{i}]pad=iw+2*{pad}:ih+2*{pad}:{pad}:{pad}:color=#00000000[v{i}];' for i in range(c * r)]) 
                    + ''.join([f'[v{i}]' for i in range(c * r)])
                    + f'xstack=inputs={c * r}:layout='
                    + '|'.join([f'{i * (width + pad * 2)}_{j * (height + pad * 2)}' for j in range(r) for i in range(c)])
                    + '[c]')
    else:
        cmd.append (
                    ''.join([f'[{i}:v:0]scale=-1:{args.height}[b{i}];\
                            [b{i}]format=rgba[c{i}];[c{i}]pad=iw+2*{pad}:ih+2*{pad}:{pad}:{pad}:color=#00000000[v{i}];' for i in range(c * r)]) 
                    + ''.join([f'[v{i}]' for i in range(c * r)])
                    + f'xstack=inputs={c * r}:layout='
                    + '|'.join([f'{i * (width + pad * 2)}_{j * (height + pad * 2)}' for j in range(r) for i in range(c)])
                    + '[c]')
        
    cmd.extend(['-map', '[c]'])
    cmd.extend(['-frames:v', '1'])
    cmd.extend(['-loglevel', 'error'])
    if args.overwrite:
        cmd.extend([output_name, '-y'])
    else:
        cmd.extend([output_name])
    return cmd

def capture_file_in_sequence(file:str, args, capture_info:dict):
    '''Captures a video according to arguments.
    To avoid memory shortage or when the command generated in capture_file_once is too long, 
    the task is accomplished by splitting the command to several sub commands.
    '''
    try:
        try:
            # Generating command
            output_name = capture_info['output_name']
            seek = capture_info['seek']
            interval = capture_info['interval']
            width, height = capture_info['width'], capture_info['height']
            c, r = capture_info['columns'], capture_info['rows']
            pad = capture_info['pad']
            fontsize = capture_info['fontsize']
            
            tmp_files = []
            tmp_dir = tempfile.gettempdir()
            # Generating images
            for i in range(c * r):
                captured = os.path.join(tmp_dir, f'{os.path.basename(output_name)}_{i}').replace('\\', SEP)
                cmd = ['ffmpeg', 
                        '-ss', f'{seek + i*interval}', '-i', file, 
                        '-filter_complex', f'[0:v:0]scale=-1:{args.height}[c]', 
                        '-map', '[c]', 
                        '-frames:v', '1', 
                        '-loglevel', 'error', 
                        '-f', 'image2', 
                        captured, '-y']
                if args.overwrite:
                    cmd.append('-y')
                _, err = run_async(cmd)
                tmp_files.append(captured)
        except Exception as e:
            [os.remove(f) for f in tmp_files]
            raise e
        
        try:
             # Generating stacking command
            cmd = ['ffmpeg']
            for i in range(c * r):
                cmd.extend(['-f', 'image2', '-i', tmp_files[i]])
            cmd.append('-filter_complex')
            if args.timestamp:
                fontfile = escape_chars(FONTFILE, r"\' =:", r'\\')
                def get_timestamp(t):
                    h, m, s = str(timedelta(seconds=t)).split(':')
                    t = f'{h}:{m}:{float(s):.3f}'
                    return escape_chars(t, r"\'=:", r'\\')
                cmd.append (
                            ''.join([f'[{i}]drawtext=fontcolor={args.fontcolor}:fontfile={fontfile}:fontsize={fontsize}:text={get_timestamp(seek + i*interval)}:x=text_h:y=text_h[b{i}];\
                                    [b{i}]format=rgba[c{i}];[c{i}]pad=iw+2*{pad}:ih+2*{pad}:{pad}:{pad}:color=#00000000[v{i}];' for i in range(c * r)]) 
                            + ''.join([f'[v{i}]' for i in range(c * r)])
                            + f'xstack=inputs={c * r}:layout='
                            + '|'.join([f'{i * (width + 2 * pad)}_{j * (height + 2 * pad)}' for j in range(r) for i in range(c)])
                            + '[c]')
            else:
                cmd.append (
                            ''.join([f'[{i}]format=rgba[c{i}];[c{i}]pad=iw+2*{pad}:ih+2*{pad}:{pad}:{pad}:color=#00000000[v{i}];' for i in range(c * r)]) 
                            + ''.join([f'[v{i}]' for i in range(c * r)])
                            + f'xstack=inputs={c * r}:layout='
                            + '|'.join([f'{i * (width + 2 * pad)}_{j * (height + 2 * pad)}' for j in range(r) for i in range(c)])
                            + '[c]')
                
            cmd.extend(['-map', '[c]'])
            cmd.extend(['-loglevel', 'error'])
            if args.overwrite:
                cmd.extend([output_name, '-y'])
            else:
                cmd.extend([output_name])
            
            # Run stacking command
            _, err = run_async(cmd)
            
            if err:
                logger.error(f'Error occured during capturing {file}:{NL}{suppress_log(err)}')
                return CaptureResult.CAPTURE_ERROR_OCCURED
            else:
                logger.info(f'Succeeded in capturing {file}.')
                return CaptureResult.SUCCEEDED
        except Exception as e:
            raise e
        finally:
            [os.remove(f) for f in tmp_files]
    except Exception:
        logger.error(suppress_log(format_exc()))
        logger.info(f'Failed to capture {file}.')
        return CaptureResult.CAPTURE_FAILED

def capture_file(file:str, args):
    '''Probe and capture a file.
    There are two ways to do that.
    (1) Compile the task into one command and run it once;
    (2) Capture all the images and save them on the disk before joining them in another command.
    
    The first way is more efficient when the file is small and the number of captures (c * r) is 
    small, but it is also more memory consuming. So this method chooses one of them to execute.
    '''
    if not os.path.isfile(file):
        logger.error(f'Specified file {file} does not exist.')
        return file, CaptureResult.PROBE_FAILED
    
    begin = datetime.now()
    try:
        # Probe file info.
        logger.info(f'Probing file {file}...')
        info = probe_file(file)
        output_name = get_output_name(file, args.format)
        
        duration = info['duration']
        seek = args.seek
        c, r = args.tile.split('x')
        c, r = int(c), int(r)
        interval = (duration - seek) / (c * r)
        size = info['size'] / (1024 * 1024)
        width, height = info['width'] * args.height / info['height'], args.height
        pad = max(int(args.padratio * min(width, height)), 0)
        fontsize = min(max(int(args.fontratio * min(width, height)), MIN_FONTSIZE), MAX_FONTSIZE)
        
        if duration < seek:
            raise ValueError(f'Invalid argument "-s/--seek". Total duration {duration} less than specified seek value {args.seek}.')
        
        info_txt = f"size: {size:.2f} MB, duration: {timedelta(seconds=info['duration'])}, ratio: { info['width']} x {info['height']}, average frame rate: {info['avg_frame_rate']:.3f}"
    except Exception:
        logger.error(suppress_log(format_exc()))
        logger.info(f'Failed to probe {file}.')
        return file, CaptureResult.PROBE_FAILED
    
    logger.info(f'Begin capturing {file} ({info_txt})...')
    capture_info = {
        'seek': seek, 
        'output_name': output_name, 
        'interval': interval, 
        'columns':c, 
        'rows':r, 
        'width': width, 
        'height': height, 
        'pad': pad, 
        'fontsize': fontsize
        }
    available_memory = psutil.virtual_memory().available / (1024 * 1024)
    
    # Select a method according to the file size and the current available memory
    if available_memory * MEMORY_PARA  > (size * c * r):
        logger.info(f'Trying to capture {file} in one command.')
        cmd = capture_file_once_cmd(file, args, capture_info)
        sum = 0
        for c in cmd:
            sum += len(c)
        if sum < MAX_COMMAND_LENGTH:
            try:
                _, err = run_async(cmd)
                if err:
                    logger.error(f'Error occured during capturing {file}:{NL}{suppress_log(err)}')
                    result = CaptureResult.CAPTURE_ERROR_OCCURED
                else:
                    logger.info(f'Succeeded in capturing {file}.')
                    result = CaptureResult.SUCCEEDED
            except Exception:
                logger.error(suppress_log(format_exc()))
                logger.info(f'Failed to capture {file}.')
                result = CaptureResult.CAPTURE_FAILED
        else:
            logger.info(f'Command too long. Switch to sequnce command mode.')
            result = capture_file_in_sequence(file, args, capture_info)
    else:
        logger.info(f'Capturing {file} in splitted commands.')
        result = capture_file_in_sequence(file, args, capture_info)
    logger.info(f'Time elapsed: {datetime.now()-begin}.')
    return file, result

def capture(file:str, args):
    '''Entry of the capture tasks.'''
    if os.path.isdir(file):
        tree_input = inspect_dir(file, None, args.overwrite, args.format)
        nodes = tree_input.walk(lambda n: (not n.is_dir()) and is_video(n.id))
        paths = [node.abs_id for node in nodes]
        if not paths:
            logger.warning(f'No files to be captured.')
            return
        logger.info(f'Number of files to be captured: {len(paths)}')
        for file in tqdm(paths):
            yield capture_file(file, args)
    else:
        yield capture_file(file, args)

def inspect_dir(dir:str, tree:NodeDir=None, overwrite=False, format='png') -> NodeDir:
    '''Retrieve a directory tree from the real directory.'''
    if tree == None:
        tree = NodeDir(dir, None)
        
    for file in os.listdir(dir):
        filename = dir + SEP + file
        if os.path.isdir(filename):
            tree.mkdir(file)
            inspect_dir(filename, tree[file], overwrite, format)
        elif is_video(file): 
            output_name = get_output_name(filename, format)
            if not os.path.exists(output_name) or overwrite:
                tree.touch(file)
    return tree

def get_output_name(file:str, format:str):
    return f'{file}.cap.{format}'

def sort_tree(tree:NodeDir):
    '''Remove unneeded branches in the tree.'''
    
    nodes = tree.walk()
    resort = False
    for node in nodes:
        if node.is_leaf():
            if node.is_dir():
                resort = True
                node.pop()
    if resort:
        sort_tree(tree)

def is_video(file:str) -> bool:
    return file.lower().strip().endswith(('.mp4', '.mkv', '.avi', '.mov', '.wmv', '.m4v', '.flv', '.rmvb', 'rm', 'ts', 'm2ts'))

def check_ffmpeg():
    '''Return the installed ffmpeg version and whether it meets the requirement.'''
    cmd = ['ffmpeg', '-version']
    try:
        out, _ = run_async(cmd)
        # \D matches non-digitals for cases like "ffmpeg version n5.0.1"
        search = re.search(r'ffmpeg version \D*(\d.\d.\d)', out, re.I)
        if search:
            version = search.group(1)
            main_version = int(version.split('.')[0])
            return main_version >= MIN_FFMPEG_MAIN_VERSION, version
        else:
            return False, 'unknown'
    except:
        return False, 'uninstalled'

if __name__ == '__main__':
    valid, version = check_ffmpeg()
    if valid:
        logger.info(f'ffmpeg {version} available.')
    else:
        logger.error(f'Not able to find a valid ffmpeg. ffmpeg with minimal version {MIN_FFMPEG_MAIN_VERSION} is required. The ffmpeg installed is {version}.')
        sys.exit(1)
    
    log_file = os.path.join(os.path.dirname(__file__), 'cap_log.log')
    log_format_console = "\n<level>{message}</level>\n"
    log_format_file = (
        "[<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>] | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>\n"
        " <level>{message}</level>\n"
        )
    logger.configure(
        handlers=[
            dict(sink=sys.stderr, format=log_format_console),
            dict(sink=log_file, rotation='16MB', encoding='utf-8', enqueue=True, retention='10 days', format=log_format_file)
        ])
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path',     type=str,   default=os.path.dirname(__file__),  help='Path of directory or file.')
    parser.add_argument('-s', '--seek',     type=float, default=0,                          help='Time of the first capture.')
    parser.add_argument('-g', '--height',   type=int,   default=270,                        help='Height of each image in the capture.')
    parser.add_argument('-t', '--tile',     type=str,   default='5x5',                      help='Tile shaple of the screen shots.')
    parser.add_argument('-o', '--overwrite',action='store_true',                            help='Whether or not overwrite existing files.')
    parser.add_argument('-i', '--timestamp',action='store_true',                            help='Whether or not show present timestamp on captures.')
    parser.add_argument('-f', '--format',   type=str,   default='png',                      help='Output format.')
    parser.add_argument('-c', '--fontcolor',type=str,   default='white',                    help='Font color of the timestamp. For example, "red" or "0#00000000".')
    parser.add_argument('-n', '--fontratio',type=float, default=0.08,                       help='Ratio of font size against short edge of each image.')
    parser.add_argument('-r', '--padratio', type=float, default=0.01,                       help='Ratio of padding against short edge of each image.')
    
    args = parser.parse_args()
    logger.info(f'Current arguments: {args}')
    
    try:
        if not os.path.exists(args.path):
            logger.error(f'Invalid argument "-p/--path". Path {args.path} does not exsist.')
            sys.exit(1)
        if args.height < 0:
            logger.error(f'Invalid argument "-g/--height". Height {args.height} invalid.')
            sys.exit(1)
        if args.seek < 0:
            logger.error(f'Invalid argument "-s/--seek". Seek {args.seek} invalid.')
            sys.exit(1)
        c, r = args.tile.split('x')
        c, r = int(c), int(r)
        if c < 1 or r < 1 or (c == 1 and r == 1):
            logger.error(f'Invalid argument "-t/--tile". Tile {args.tile} invalid.')
            sys.exit(1)
        if args.padratio < 0:
            args.padratio = 0.01
        if args.fontratio < 0:
            args.fontratio = 0.08
        if debugger_is_active():
            args.overwrite = True
            args.timestamp = True
    except Exception:
        logger.error(f'Failed to parse arguments.')
        sys.exit(1)
    
    args.path = args.path.replace('\\', SEP)
    begin = datetime.now()
    logger.info(f'Task start at {begin}.')
    
    output = list(capture(args.path, args=args))
    if output:
        count_succeeded = 0
        count_failed = 0
        count_error = 0
        for file, result in output:
            if result == CaptureResult.SUCCEEDED:
                count_succeeded += 1
            elif result == CaptureResult.CAPTURE_ERROR_OCCURED:
                count_error += 1
            else:
                count_failed += 1
        
        # Reporting result
        logger.info(NL.join([f'{result}:\t{file}' for file, result in output]))
        logger.info(f'Succeeded: {count_succeeded}{NL}' 
                    + f'Completed with error: {count_error}{NL}' 
                    + f'Failed: {count_failed}')
    
    end = datetime.now()
    logger.info(f'Task end at {end}. Total time elapsed: {end-begin}.')
    
从tqdm导入tqdm