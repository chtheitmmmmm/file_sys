from kivy.app import *
from kivy.uix.relativelayout import *
from PIL import Image, ImageDraw, ImageFont
from kivy.uix.image import Image as IMG
import math
import io

fnt = ImageFont.truetype(open('pingfang.ttf', 'rb'), 10)
ImageDraw.ImageDraw.font = fnt
ImageFont.ImageFont.font = fnt
Fonter = ImageFont.ImageFont()

src = Image.open('person.png').convert("RGBA")
ctt = "亚里士多德"
opc = 100
ang = 30
gap = fnt.size
color = (0, 0, 0)
te = Image.new("RGBA", (max(Fonter.getsize(ctt)), ) * 2, (255, 255, 255, 0))
drawte = ImageDraw.Draw(te)
drawte.text((0, (te.height - fnt.size)  / 2), ctt, fill=(*color, opc))
te = te.rotate(ang)
size = te.size
texts = Image.new("RGBA", src.size, (255, 255, 255, 0))
drawtexts = ImageDraw.Draw(texts)
for line in range(0, src.width, int(size[0] + gap)):
    for col in range(0, src.height, int(size[1] + gap)):
        texts.paste(te, (col, line))

texts.show()
print(texts.mode, src.mode)
src = Image.alpha_composite(src, texts)
src = src.resize((500, src.size[1] * 500 // src.size[0]))
f = io.BytesIO()
src.save(f,"PNG")
f.seek(0)
io.FileIO('water_person.png', "wb").write(f.read())

src.show()

class MyRoot(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        i = IMG(source="water_person.png")
        i.texture_size = i.texture_size[0] * 2, i.texture_size[1] * 2

        self.add_widget(i)
    pass

class MyApp(App):
    def build(self):
        return MyRoot()
    pass

MyApp().run()