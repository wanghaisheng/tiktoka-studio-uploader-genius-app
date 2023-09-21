import pandas as pd
import json
from PIL import Image, ImageDraw, ImageFont,ImageColor
import os
import sys

def calculate_text_size(text, font):
    width, height = font.getsize(text)
    return width, height

def calculate_text_lines(text, font, max_width):
    lines = []
    words = text.split()
    current_line = words[0]
    for word in words[1:]:
        line_width, _ = calculate_text_size(current_line + " " + word, font)
        if line_width <= max_width:
            current_line += " " + word
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    return lines

def convert_canvas_coord_to_corner(canvas_coord, zone_width, zone_height):
    zone_number = canvas_coord - 1
    zone_column = zone_number % 4
    zone_row = zone_number // 4
    corner_x = zone_column * zone_width
    corner_y = zone_row * zone_height
    return corner_x, corner_y

def draw_multiline_text(draw, text, start_coord, font, max_width, font_size, font_color):
    lines = calculate_text_lines(text, font, max_width)
    x, y = start_coord
    # font = ImageFont.truetype(font, size=int(font_size))
    for line in lines:
        draw.text((x, y), line, font=font, fill=font_color)
        x, y = start_coord[0], y + font.getsize(line)[1]

def clean_column_name(column_name):
    return column_name.replace(" ", "_")

def validate_font_path(font_file):
    try:
        ImageFont.truetype(font_file)
        return True
    except (OSError, FileNotFoundError):
        return False

def get_default_font(language):
    default_fonts = {
        "win32": {
            "en": "arial.ttf",
            "es": "arial.ttf",
            "zh": "simhei.ttf"
        },
        "darwin": {
            "en": "/Library/Fonts/Arial.ttf",
            "es": "/Library/Fonts/Arial.ttf",
            "zh": "/Library/Fonts/SimHei.ttf"
        },
        "linux2": {
            "en": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "es": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "zh": "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"
        }
    }

    platform = sys.platform
    if platform in default_fonts:
        return default_fonts[platform].get(language, default_fonts[platform]["en"])
    else:
        return default_fonts["win32"]["en"]

def load_font(font_name,font_file, font_size, default_language):
    try:
        font = ImageFont.truetype(font_name, size=int(font_size))
    except (OSError, FileNotFoundError):

        try:
            font = ImageFont.truetype(font_file, size=int(font_size))
        except (OSError, FileNotFoundError):
            font = ImageFont.truetype(get_default_font(default_language), size=int(font_size))
    return font


def validateSeting(setting):
    thumb_gen_setting = setting
    
    result_image_width = thumb_gen_setting.get("result_image_width", 1480)
    result_image_height = thumb_gen_setting.get("result_image_height", 920)
    template_path = thumb_gen_setting.get("template_path", "")
    template_data=thumb_gen_setting.get("texts")
    # Load and validate the template settings
    # Check if template data is empty or a JSON string
    if not template_data or template_data == '[]':
        try:
            with open(template_path, "r", encoding="utf-8") as template_file:
                template_data = json.load(template_file).get('texts', [])
        except FileNotFoundError:
            print("Error: Template file not found.")
        except json.JSONDecodeError:
            print("Error: Invalid JSON format in the template file.")




    for template_item in template_data:
        text_type = template_item.get("textType", "")
        font_file = template_item.get("fontFile", "")
        x = template_item.get("x", 0)
        y = template_item.get("y", 0)
        width = template_item.get("width", 0)
        height = template_item.get("height", 0)
        top_left = template_item.get("topLeft", "")
        top_right = template_item.get("topRight", "")
        bottom_left = template_item.get("bottomLeft", "")
        bottom_right = template_item.get("bottomRight", "")
        font_size = template_item.get("fontSize", 0)
        font_name = template_item.get("fontName", "")
        grid_size = template_item.get("gridSize", 0)
        nearest_grid_serial_number = template_item.get("nearestGridSerialNumber", 0)
        font_color = template_item.get("fontcolor", "")
        try:
            font = ImageFont.truetype(font_name, size=int(font_size))
        except (OSError, FileNotFoundError):
            print(f'cannot find font named {font_name}')

        # Validate font file
        if font_file:
            if not validate_font_path(font_file):
                print(f"Warning: Font file '{font_file}' is invalid or cannot be found. Using default font.")
                font_file = ""



        # Validate coordinates
        if not (0 <= x < result_image_width) or not (0 <= y < result_image_height):
            print(f"Warning: Invalid coordinates for '{text_type}' - (x, y) out of image bounds. Skipping.")
            continue

        # Validate and parse coordinate format (topLeft, topRight, bottomLeft, bottomRight)
        try:
            top_left = tuple(map(int, top_left.strip("()").split(", ")))
            top_right = tuple(map(int, top_right.strip("()").split(", ")))
            bottom_left = tuple(map(int, bottom_left.strip("()").split(", ")))
            bottom_right = tuple(map(int, bottom_right.strip("()").split(", ")))
        except ValueError:
            print(f"Warning: Invalid coordinate format for '{text_type}'. Skipping.")
            continue

        # Validate font size
        if not (0 < font_size <= 200):
            print(f"Warning: Invalid font size for '{text_type}'. Using default font size.")
            font_size = 12

        # Validate font color (support color_name|hex_number|rgb_number)
        if not font_color:
            print(f"Warning: Font color not specified for '{text_type}'. Using default color (black).")
            font_color = "black"
        else:
            try:
                # Try to parse color as a tuple (R, G, B)
                font_color = tuple(map(int, font_color.strip("rgb()").split(",")))
                if len(font_color) != 3 or not all(0 <= c <= 255 for c in font_color):
                    raise ValueError
            except ValueError:
                # If parsing as tuple fails, treat font_color as a named color or hex color
                font_color = font_color.lower()  # Convert to lowercase for named colors
                if not font_color.startswith("#") and font_color not in ImageColor.colormap:
                    print(f"Warning: Invalid font color '{font_color}' for '{text_type}'. Using default color (black).")
                    font_color = "black"
    return thumb_gen_setting

def draw_text_on_image(row,thumb_gen_setting,result_image_width,result_image_height, render_style,output_folder,filename):

    thumbnail_bg_image_path=row.get('thumbnail_bg_image_path')


    # Calculate rendering style based on configuration (topLeft or grid)
    # Create a new image with the specified dimensions
    canvas_image = Image.new("RGB", (result_image_width, result_image_height))

    # Create a drawing object
    draw = ImageDraw.Draw(canvas_image)

    # Load and resize the background image
    if thumbnail_bg_image_path:
        bg_image = Image.open(thumbnail_bg_image_path)
        bg_image = bg_image.resize((result_image_width, result_image_height), Image.ANTIALIAS)  # Resize

        # Overlay the background image on the canvas
        canvas_image.paste(bg_image, (0, 0))

    for template_element in thumb_gen_setting:
        x, y = map(int, template_element["topLeft"].strip("()").split(", "))
        max_width = template_element["width"]
        font_size = template_element["fontSize"]
        font_color = template_element["fontcolor"]
        text_type = template_element["textType"]
        font_name = template_element["fontName"]
        nearest_grid_serial_number = template_element["nearestGridSerialNumber"]
        font_file = template_element["fontFile"]

        grid_size = template_element["gridSize"]
        # Load the font
        font = load_font(font_name,font_file, font_size, "en")
        if row[text_type]:
            if render_style== 'cord':
                # Render using topLeft as the starting point
                draw_multiline_text(draw, row[text_type], (x, y), font, max_width, font_size,font_color)
            else:
                # Render using nearestGridSerialNumber and gridSize to calculate coordinates
                corner_x, corner_y = convert_canvas_coord_to_corner(
                    nearest_grid_serial_number, result_image_width // grid_size, result_image_height // grid_size
                )
                draw_multiline_text(draw, row[text_type], (corner_x , corner_y), font, max_width, font_size,font_color)
        #save image to output folder with filename
    # Save the image to the output folder with the specified filename
    print('save dir',output_folder)
    print('thumbnail filename',filename)

    output_path = os.path.join(output_folder, filename)
    canvas_image.save(output_path)
def overlay_gridlines(image, width, height):
    draw = ImageDraw.Draw(image)
    for x in range(width // 10, width, width // 10):
        draw.line([(x, 0), (x, height)], fill="red", width=1)
    for y in range(height // 10, height, height // 10):
        draw.line([(0, y), (width, y)], fill="red", width=1)


def main():
    output_folder = "output"  # Replace with your desired output folder path
    os.makedirs(output_folder, exist_ok=True)


    # Process video data (if available)
    video_data_json_str = """
 {
            "1": {
                "captions_certification": 0,
                "heading": "xxxxx",
                "thumbnail_bg_image_path": "D:/Download/audio-visual/saas/tiktoka/tiktoka-studio-uploader-app/tests/videos/1/sp/1-002.jpg",
                "subheading": "yyy"
            },
            "2": {
                "captions_certification": 0,
                "heading": "sssss",
                "subheading": "zzzzz"
            }
        }
    """
    setting_str="""
{
        "width": 1080,
        "height": 1920,
        "texts": [
                {
                        "textType": "heading",
                        "fontFile": "",
                        "x": 216,
                        "y": 336,
                        "width": 599,
                        "height": 140,
                        "topLeft": "(216, 336)",
                        "topRight": "(815, 336)",
                        "bottomLeft": "(216, 476)",
                        "bottomRight": "(815, 476)",
                        "fontSize": 35,
                        "fontName": "Unknown",
                        "gridSize": 10,
                        "nearestGridSerialNumber": 13,
                        "fontcolor": "rgb(24, 78, 164)"
                },
                {
                        "textType": "subheading",
                        "fontFile": "",
                        "x": 288,
                        "y": 1298,
                        "width": 473,
                        "height": 105,
                        "topLeft": "(288, 1298)",
                        "topRight": "(761, 1298)",
                        "bottomLeft": "(288, 1403)",
                        "bottomRight": "(761, 1403)",
                        "fontSize": 26,
                        "fontName": "Unknown",
                        "gridSize": 10,
                        "nearestGridSerialNumber": 63,
                        "fontcolor": "rgb(24, 78, 164)"
                }
        ]
}
"""

    template_data=validateSeting(json.loads(setting_str))
    video_data = json.loads(video_data_json_str)
    render_style=template_data.get("render_style") 
    result_image_width=int(template_data.get('result_image_width'))
    result_image_height=int(template_data.get('result_image_height'))        

    for video_id, video_info in video_data.items():
        print('1',video_info)
        thumb_gen_setting = template_data.get("template", [])

        ext='.png'
        dict_9_16={
            'xhs':"1080*1440px",
            'dy':"1080*1920px",
            'wx':"1080*1260px",
            'youtube':"1280*720",
            'tiktok':"1080*1920px"

        }
        dict_16_9={
            'xhs':"1440*1080px",
            'dy':"1080*608px",
            'wx':"1080*608px",
            'youtube':"1920 * 1080",
            'tiktok':"1080*608px"


        }

        filename=video_id+ext
        filename=video_id+"_"+str(result_image_width)+"x"+str(result_image_height)+ext
        draw_text_on_image(video_info,thumb_gen_setting,result_image_width,result_image_height,render_style,output_folder,filename)

        if result_image_width > result_image_height:
            basedir=output_folder+os.sep+'16-9'
            os.makedirs(basedir, exist_ok=True)

            # 16:9 aspect ratio        
            for key,value in dict_16_9.items():
                output_folder=basedir+os.sep+key
                os.makedirs(output_folder, exist_ok=True)
                filename=video_id+ext
                value=value.replace("px","")
                result_image_width=int(value.split("*")[0])
                result_image_height=int(value.split("*")[-1])
                filename=video_id+"_"+value.replace("*","x")+ext

                draw_text_on_image(video_info,thumb_gen_setting,result_image_width,result_image_height,render_style,output_folder,filename)
        else:
            # 9:16 aspect ratio    
            basedir=output_folder+os.sep+'9-16'

            os.makedirs(basedir, exist_ok=True)
            for key,value in dict_9_16.items():
                output_folder=basedir+os.sep+key
                os.makedirs(output_folder, exist_ok=True)
                filename=video_id+ext
                value=value.replace("px","")
                result_image_width=value.split("*")[0]
                result_image_height=value.split("*")[-1]
                filename=video_id+"_"+value.replace("*","x")+ext

                draw_text_on_image(video_info,thumb_gen_setting,result_image_width,result_image_height,render_style,output_folder+os.sep+'9-16'+os.sep+key,filename)
if __name__ == "__main__":
    main()
