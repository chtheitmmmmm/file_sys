from kivy.properties import *
from ....fileinfopages.filesviewpage.fileitemspage import FileItemsPage, FileItemsPageLayuot
from statemachine_decorator import state_define
from promise.promise import Promise
from kivy.uix.button import ButtonBehavior
from kivy.uix.label import *
from kivy.graphics import Color, Rectangle
import  sysapp

class MyFileItemsPage(FileItemsPage):
    pass

class MyFileItemsPageLayoutUploadButton(ButtonBehavior, Label):
    def _do_press(self):
        with self.canvas.before:
            Color(67 / 255, 136 / 255, 75 / 255, 1)
            Rectangle(pos=self.pos, size=self.size)

    def _do_release(self, *args):
        with self.canvas.before:
            Color(116 / 255, 233 / 255, 130 / 255, 1)
            Rectangle(pos=self.pos, size=self.size)

@state_define({
    "plain": {"uploading"},
    "uploading": {"plain"}
}, "plain")
class MyFileItemsPageLayout(FileItemsPageLayuot):
    STATE = StringProperty('plain')

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.register_event_type("on_upload")

    def SWITCH(self, name):
        self.switch(name)
        self.STATE = self.state

    def on_upload(self):
        self.SWITCH('uploading')
        Promise().resolve(None) \
            .then(lambda v:  sysapp.sysapp.user.upload_file()) \
            .then(lambda v:  sysapp.sysapp.show_success_toast('上传成功') if v else '') \
            .then(lambda v: self.dispatch("on_refresh"))\
            .catch(lambda e:  sysapp.sysapp.show_error_toast(str(e))) \
            .then(lambda v: self.SWITCH("plain"))

__all__ = ("MyFileItemsPage", "MyFileItemsPageLayout", "MyFileItemsPageLayoutUploadButton")