from kivy.uix.switch import Switch
from kivy.app import *
from kivy.properties import *
from kivy.uix.relativelayout import RelativeLayout


class Root(RelativeLayout):
    ac = BooleanProperty(True)

class MySwitch(Switch):
    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.active = False

class TogApp(App):
    pass


TogApp().run()