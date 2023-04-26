from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.app import runTouchApp
from kivy.graphics import Color, Rectangle

class L(Label):
    def __init__(self, **kwargs):
        super(L, self).__init__(**kwargs)
        with self.canvas.before:
            Color(1, 1, 1, 1)
            Rectangle(pos=self.pos, size=self.size)

layout = GridLayout(cols=1, spacing=10, size_hint_y=None, height=2000)
# Make sure the height is such that there is something to scroll.
layout.bind(minimum_height=layout.setter('height'))
l = L(text="hello\nworld!\n" * 200, size_hint_y = None, color="green", height=200, width=1000)

root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height), always_overscroll=True,
                  do_scroll_x=False, effect_cls="ScrollEffect")
root.add_widget(l)

runTouchApp(root)