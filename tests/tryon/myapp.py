from kivy.app import *
from kivy.uix.relativelayout import *

"""
在 kivy 中，用 kv 文件初始化kivy规则不会导致相关事件被触发
"""

class MyApp(App):
    pass

MyApp().run()