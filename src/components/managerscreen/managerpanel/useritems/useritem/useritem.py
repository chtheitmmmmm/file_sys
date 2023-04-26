from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import *
from kivy.graphics import Color, Rectangle

class UserItem(RelativeLayout):
    master_user = ObjectProperty(None, force_dispatch=True) # 用户对象 TODO: 系统登入时前将从数据库中加载用户对象列表

__all__ = ("UserItem",)