from kivy.uix import *
from kivy.app import *


class Sup(BoxLayout):
    pass

class Sub(Sup):
    pass
class TestApp(App):
    def build(self):
        return Sub()


TestApp().run()