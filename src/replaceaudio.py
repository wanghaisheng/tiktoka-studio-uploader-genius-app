# https://raw.githubusercontent.com/Adillwma/ffAudioMUX/main/ffAudioMUX_v1.py
import tkinter as tk
from tkinter import filedialog
import subprocess
import os
import subprocess
import os
import shutil

def find_ffmpeg():
    # Define the possible installation paths
    possible_folders = [
        r'C:\Program Files\ffmpeg\\',
        r'C:\Program Files (x86)\ffmpeg\\',
        r'C:\Program Files\\',
        r'C:\Program Files (x86)\\',
    ]

    def find_ffmpeg_recursive(folder):
        for root, dirs, files in os.walk(folder):
            if 'ffmpeg.exe' in files:
                return os.path.join(root, 'ffmpeg.exe')
        return None

    # Try to find ffmpeg.exe in the predefined folders and their subfolders
    ffmpeg_path = None

    for folder in possible_folders:
        ffmpeg_path = find_ffmpeg_recursive(folder)
        if ffmpeg_path:
            break

    # Save the found path to a file for future use (even if it was found in predefined folders)
    if ffmpeg_path:
        with open('ffmpeg_path.txt', 'w') as f:
            f.write(ffmpeg_path)

    return ffmpeg_path

def get_ffmpeg():
    # Specify the URL of the gyan.dev repository
    ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"

    # Specify the directory where you want to install FFmpeg
    install_dir = "C:\Remove\\"

    # create the directory if it doesn't exist
    os.makedirs(install_dir, exist_ok=True)

    # Define the command to download and extract the FFmpeg binaries
    download_command = [
        "curl",
        "-L",
        "-o",
        "ffmpeg.zip",
        ffmpeg_url,
    ]
    extract_command = [
        "tar",
        "xf",
        "ffmpeg.zip",
        "-C",
        install_dir,
    ]

    # Run the download and extract commands
    try:
        subprocess.run(download_command, check=True)
        subprocess.run(extract_command, check=True)

        # Find the subdirectory in the installation directory
        subdirs = [d for d in os.listdir(install_dir) if os.path.isdir(os.path.join(install_dir, d))]

        if len(subdirs) == 1:
            subdir_name = subdirs[0]
            
            # Move all files and subdirectories from the subdirectory to the main directory
            subdir_path = os.path.join(install_dir, subdir_name)
            for item in os.listdir(subdir_path):
                item_path = os.path.join(subdir_path, item)
                if os.path.isfile(item_path) or os.path.isdir(item_path):
                    shutil.move(item_path, install_dir)

            # Remove the now-empty subdirectory
            os.rmdir(subdir_path)

            
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")



def your_function2():
    global video_file_loaded, video_file_path

    video_file_path = filedialog.askopenfilename(title="Select a video file", filetypes=([("Video Files", "*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm *.ogg *.ogv *.mpeg *.mpg *.m4v *.3gp *.3g2 *.ts *.vob *.mxf *.tsv *.mts *.m2ts *.m2v *.divx *.f4v *.rmvb *.asf *.rm *.m1v *.m2v *.m2t *.amv *.mpv *.nut *.dv *.drc")]))
    print(f"Selected file: {video_file_path}")

    video_file_loaded = True
    check_if_MUX_allowed()

def your_function3():
    global audio_file_loaded, audio_file_path

    audio_file_path = filedialog.askopenfilename(title="Select a audio file", filetypes=([("Audio Files", "*.ac3 *.eac3 *.flac *.ape *.aac *.wma *.pcm *.wav *.mp3 *.m4a *.ogg *.oga *.wv *.tta *.mka *.opus *.ra *.aif *.aiff *.caf *.au *.alac *.mpc *.tak *.shn *.wv *.wma *.aac *.m4a *.dts *.dtshd *.w64 *.sds")]))
    print(f"Selected file: {audio_file_path}")

    audio_file_loaded = True
    check_if_MUX_allowed()

def your_function4():
    global output_directory_loaded, output_file_path
    # Extract the file extension from the loaded video path3
    file_extension = os.path.splitext(video_file_path)[-1]

    output_file_path = filedialog.asksaveasfilename(defaultextension=file_extension, title="Select a output file location", filetypes=[("Video file", file_extension)])
    print(f"Selected file location: {output_file_path}")

    output_directory_loaded = True
    check_if_MUX_allowed()

def your_function5():
    command = [ffmpeg_path, '-i', f'{video_file_path}', '-i', f'{audio_file_path}', '-c:v', 'copy', '-map', '0:v:0', '-map', '1:a:0', f'{output_file_path}']

    # Run the command
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True)

    ffmpeg_label6.config(text="Task Complete!")
    # Print the output of the command
    print(result.stdout)

    print("Audio MUX processing...")

def check_if_MUX_allowed():
    if ffmpeg_loaded and video_file_loaded and audio_file_loaded and output_directory_loaded:
        button4.config(state=tk.NORMAL) # Enable the MUX button




video_file_loaded = False
audio_file_loaded = False
output_directory_loaded = False

# Check for prexisting FFmpeg installation
ffmpeg_path = find_ffmpeg()
if ffmpeg_path:
    ffmpeg_loaded = True
else:
    get_ffmpeg()
    find_ffmpeg()
    if ffmpeg_path:
        ffmpeg_loaded = True

root = tk.Tk()

# Set the default window size to 400x300 pixels
root.geometry("300x340")

root.title("ffAudioMUX v1.0")

ffmpeg_label1 = tk.Label(root, text="FFmpeg check")
ffmpeg_label1.pack()

ffmpeg_label2 = tk.Label(root, text=f"FFmpeg found: {ffmpeg_loaded}")
ffmpeg_label2.pack()

# Add vertical space between widgets using empty labels
spacer = tk.Label(root, text="", height=2)
spacer.pack()

button1 = tk.Button(root, text="Select Video File...", pady=10, command=your_function2)
button1.pack()

button2 = tk.Button(root, text="Select Audio File...", pady=10, command=your_function3)
button2.pack()

button3 = tk.Button(root, text="Select Output Directory", pady=10, command=your_function4)
button3.pack()

# Add vertical space between widgets using empty labels
spacer = tk.Label(root, text="", height=1)
spacer.pack()

button4 = tk.Button(root, text="RUN the MUX", pady=10, state=tk.DISABLED, command=your_function5)
button4.pack()

ffmpeg_label6 = tk.Label(root, text="")
ffmpeg_label6.pack()

# Center all widgets vertically and horizontally
root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f'{width}x{height}+{x}+{y}')

# Start the GUI
root.mainloop()


