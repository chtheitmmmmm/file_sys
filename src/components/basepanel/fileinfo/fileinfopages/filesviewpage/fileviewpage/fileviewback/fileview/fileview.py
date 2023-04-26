from kivy.uix.relativelayout import *
from kivy.properties import *
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from promise.promise import Promise
import  sysapp

class FileView(ScrollView):
    file = ObjectProperty(None)  # 文件对象

    def on_touch_down(self, touch):
        super(FileView, self).on_touch_down(touch)
        return False

class FileViewLayout(RelativeLayout):
    file = ObjectProperty(None)
    content = StringProperty('未知内容')
    name = StringProperty('未知标题')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(file=self.on_file)
        self.file = self.file

    def on_file(self, *args):
        self.name = self.file.name
        loading =  sysapp.sysapp.show_loading_toast('打开中')
        Promise.resolve(self.file)\
            .then(lambda f: setattr(self, 'content', self.file.content))\
            .catch(lambda e:  sysapp.sysapp.show_error_toast(str(e)))\
            .then(lambda v: loading.dismiss())


__all__ = ("FileView", "FileViewLayout")