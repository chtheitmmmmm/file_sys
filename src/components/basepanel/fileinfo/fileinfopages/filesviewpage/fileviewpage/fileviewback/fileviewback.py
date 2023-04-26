from kivy.uix.relativelayout import RelativeLayout
from .......superbutton import SuperButton
from kivy.properties import *
from kivy.uix.button import ButtonBehavior
from kivy.uix.label import *
from kivy.uix.textinput import TextInput
from promise.promise import Promise
import  sysapp
from tkinter.filedialog import asksaveasfilename
from .printsetting import PrintSetting


class FileViewPrintButton(SuperButton):
    pass

class FileViewBackButton(ButtonBehavior, Label):
    pass

class FileViewBack(RelativeLayout):
    file = ObjectProperty(None)

    def on_kv_post(self, base_widget):
        self.register_event_type("on_back")
        self.register_event_type("on_print")

    def on_back(self):
        self.parent.dispatch("on_back")

    def on_print(self):
        Promise.resolve(None)\
            .then(lambda v: self._print())

    def _print(self):
        pst = PrintSetting(file_view=self.children[0].children[0].children[0])
        pst.open()

__all__ = ("FileViewBack", "FileViewBackButton", "FileViewPrintButton")
