from PIL import Image, ImageDraw, ImageFont

# get an image
with Image.open("person.png").convert("RGBA") as base:

    # make a blank image for the text, initialized to transparent text color
    txt = Image.new("RGBA", base.size, (255, 255, 255, 0))

    # get a font
    fnt = ImageFont.truetype(open('pingfang.ttf', 'rb'), 40)
    # get a drawing context
    d = ImageDraw.Draw(txt)

    # draw text, half opacity
    d.text((50, 10), "Hello", font=fnt, fill=(255, 255, 255, 128))
    # draw text, full opacity
    d.text((60, 60), "World", font=fnt, fill=(255, 255, 255, 255))
    txt = txt.rotate(-45)
    out = Image.alpha_composite(base, txt)

    out.show()