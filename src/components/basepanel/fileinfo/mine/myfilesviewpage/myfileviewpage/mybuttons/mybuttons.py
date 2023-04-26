from kivy.uix.boxlayout import BoxLayout
from kivy.properties import *

class MyButtons(BoxLayout):
    file = ObjectProperty(None)
    def __init__(self, **kwargs):
        self.register_event_type("on_send")
        self.register_event_type("on_encrypt")
        self.register_event_type("on_delete")
        super(MyButtons, self).__init__(**kwargs)

    def on_send(self, file):
        self.parent.dispatch('on_send', file)

    def on_encrypt(self, file):
        self.parent.dispatch('on_encrypt', file)

    def on_delete(self, file):
        self.parent.dispatch('on_delete', file)

__all__ = ("MyButtons", )
