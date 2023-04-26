from kivy.app import App
from kivy.core.window import Window
from sysscreens import SysScreens
from kivy.properties import *
from components import *
import entities

class SysApp(App):
    user = ObjectProperty(None, force_dispatch=True)     # 用户数据库
    users = ObjectProperty(None, force_dispatch=True)    # 所有用户的数据库

    def __init__(self, **kwargs):
        self.users = entities.Users("database/users")
        self.logger = entities.Logger(master_user=self.user)
        self.icon = "resource/graphics/sysicon.png"
        super(SysApp, self).__init__(**kwargs)

    def on_start(self):
        self.window = Window

    def on_stop(self):
        self.users.close()

    def show_success_toast(self, msg: str):
        t = SuccessToast(msg=msg)
        t.open()

    def show_error_toast(self, msg: str):
        t = ErrToast(msg=msg)
        t.open()

    def show_loading_toast(self, msg: str="请稍等"):
        t = LoadingToast(msg=msg)
        t.open()
        return t    # then hide t

sysapp = SysApp()   # 全局 app 对象
sysapp.load_kv('sys.kv')
