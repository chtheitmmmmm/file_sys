from kivy.uix.boxlayout import BoxLayout
from kivy.properties import *
from kivy.uix.screenmanager import *
from kivy.uix.button import ButtonBehavior
from kivy.uix.label import *
from kivy.graphics import Color, Rectangle
from ......superbutton import SuperButton


class FileViewButton(SuperButton):
    pass

class FileViewPage(Screen):
    file = ObjectProperty(None)

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.register_event_type('on_back')

    def on_back(self):
        self.parent.dispatch("on_back")

class FileViewPageLayout(BoxLayout):
    file = ObjectProperty(None)

    def on_kv_post(self, base_widget):
        super(FileViewPageLayout, self).on_kv_post(base_widget)
        self.register_event_type('on_back')

    def on_back(self):
        self.parent.dispatch("on_back")

__all__ = ("FileViewPage", "FileViewPageLayout", "FileViewButton")