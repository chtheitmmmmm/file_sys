from kivy.uix.button import ButtonBehavior
from kivy.uix.label import Label
from kivy.properties import *
from kivy.graphics import *

class SuperButton(ButtonBehavior, Label):
    press_color = ListProperty([1, 1, 1, 0.5])
    plain_color = ListProperty([0, 0, 0, 1])
    def _do_press(self):
        super()._do_press()
        with self.canvas.before:
            Color(*self.press_color)
            Rectangle(pos=self.pos, size=self.size)
    def _do_release(self, *args):
        super()._do_release(*args)
        with self.canvas.before:
            Color(*self.plain_color)
            Rectangle(pos=self.pos, size=self.size)