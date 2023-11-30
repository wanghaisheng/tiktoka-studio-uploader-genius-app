from PIL import Image, ImageDraw, ImageFont,ImageFilter
import itertools
import os
# 创建一个新的画布
image = Image.new('RGB', (1280, 720), (255, 255, 255))
fonts=r'C:\Windows\fonts\simsun.ttc'


#setting varibles
imgFile = "frame_0.jpg"

font = ImageFont.truetype("arial.ttf", 60)
text = "DRAG RACE"
textColor = 'white'
shadowColor = 'black'
outlineAmount = 3

#open image
# img = Image.open(imgFile)
img =image
draw = ImageDraw.Draw(img)

#get the size of the image
imgWidth,imgHeight = img.size

#get text size
txtWidth, txtHeight = draw.textsize(text, font=font)

#get location to place text
x = imgWidth - txtWidth - 400
y = imgHeight - txtHeight - 400

def raw():
        #create outline text
        for adj in range(outlineAmount):
                #move right
                draw.text((x-adj, y), text, font=font, fill=shadowColor)
                #move left
                draw.text((x+adj, y), text, font=font, fill=shadowColor)
                #move up
                draw.text((x, y+adj), text, font=font, fill=shadowColor)
                #move down
                draw.text((x, y-adj), text, font=font, fill=shadowColor)
                #diagnal left up
                draw.text((x-adj, y+adj), text, font=font, fill=shadowColor)
                #diagnal right up
                draw.text((x+adj, y+adj), text, font=font, fill=shadowColor)
                #diagnal left down
                draw.text((x-adj, y-adj), text, font=font, fill=shadowColor)
                #diagnal right down
                draw.text((x+adj, y-adj), text, font=font, fill=shadowColor)

        #create normal text on image
        draw.text((x,y), text, font=font, fill=textColor)


        output = "frame_edit_1.jpg"
        img.save(output)
        os.startfile(output)
def raw2():

        draw.text((x, y), text, font=font, fill=textColor,stroke_width=outlineAmount, stroke_fill=shadowColor)   
        output = "frame_edit_2.jpg"

        img.save(output)
        os.startfile(output)
raw2()
raw()