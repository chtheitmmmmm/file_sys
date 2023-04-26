from kivy.app import *
from kivy.uix import *

class M1(ModalView):
    pass

class M2(ModalView):
    pass

class MultiModalApp(App):
    def build(self):
        M2().open()
        M1().open()
        return RelativeLayout()

MultiModalApp().run()