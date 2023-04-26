from kivy.uix import *
from kivy.app import App

class MyEventDispatcher(BoxLayout):
    def __init__(self, **kwargs):
        # self.register_event_type('on_test')
        super(MyEventDispatcher, self).__init__(**kwargs)
        self.add_widget(Son(text="world"))

        self.add_widget(Son(text='hello'))
        self.bind(on_test=lambda v: print('father recieve'))
    def do_something(self, value):
# when do_something is called, the 'on_test' event will be # dispatched with the value
        self.children[0].dispatch('on_test', value)

    def on_test(self, *args):
        print("me recieve")

    def on_release(self, *args):
        self.do_something(args)

class Son(Button):
    def __init__(self, **kwargs):
        super(Son, self).__init__(**kwargs)
        self.register_event_type('on_test')

    def on_touch_down(self, touch):
        print('touch down')
        self.dispatch("on_test")

    def on_test(self, *args):
        # 默认处理函数必须添加
        print("I am dispatched", self.text)
        return False

class PtApp(App):
    def build(self):
        return MyEventDispatcher()
    
PtApp().run()