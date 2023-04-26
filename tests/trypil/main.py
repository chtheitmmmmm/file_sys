from PIL import Image, PSDraw, ImageEnhance, ImageFilter, ImageFont, ImageDraw

import sys
import io
from PIL import Image, ImageDraw
fnt = ImageFont.truetype(open('pingfang.ttf', 'rb'), 40)
ImageDraw.ImageDraw.font = fnt
ImageFont.ImageFont.font = fnt
print(ImageFont.ImageFont().getsize("你好\n我爱你\n再见"))
m = ImageFont.ImageFont()
with Image.open("person.png") as im:
    ImageDraw.ImageDraw.fill = True
    draw = ImageDraw.Draw(im)
    draw.line((0, 0) + im.size, fill=(1, 100, 23, 1), width=10)
    draw.line((0, im.size[1], im.size[0], 0), fill=128)
    draw.fill=False
    draw.text((132, 10), "你好\n我爱你\n再见", fill=(23,100, 200, 1), )
    # write to stdout
    draw.arc([0, 0, 100, 100], 0, 400, "green", width=20)
    im.save("person2.png")
    im.show()