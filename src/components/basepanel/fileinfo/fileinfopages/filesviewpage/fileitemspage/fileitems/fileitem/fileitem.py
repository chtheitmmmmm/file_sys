from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import *
from kivy.graphics import Color, Rectangle
from pathlib import Path
from kivy.uix.label import Label
from statemachine_decorator import state_define
from kivy.uix.button import ButtonBehavior


class FileItem(ButtonBehavior, RelativeLayout):
    """一个文件项"""
    selected = BooleanProperty(False)
    file = ObjectProperty(None)
    def on_select(self):
        if not self.selected:
            self.selected = True
            with self.children[-1].canvas.before:
                Color(75 / 255, 94 / 255, 241 / 255, 1)
                Rectangle(pos=self.children[-1].pos, size=self.children[-1].size)

    def on_unselect(self):
        if self.selected:
            self.selected = False
            with self.children[-1].canvas.before:
                Color(179 / 255, 179 / 255, 179 / 255, 1)
                Rectangle(pos=self.children[-1].pos, size=self.children[-1].size)

    def _do_press(self):
        if self.selected:
            # 当再次点击被选中的 fileitem，则进入查看文件的模式
            self.parent.parent.dispatch('on_view', self.file)
        else:
            self.dispatch("on_select")
            for item in self.parent.children:
                if not item is self:
                    item.dispatch("on_unselect")

    def on_kv_post(self, base_widget):
        super(FileItem, self).on_kv_post(base_widget)
        self.register_event_type('on_select')
        self.register_event_type("on_unselect")





__all__ = ("FileItem",)
