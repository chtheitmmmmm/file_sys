from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.modalview import ModalView
from kivy.uix.button import Button
from kivy.app import App
class MyApp(App):
    def build(self):
        r = RelativeLayout()
        r.add_widget(Label(
            text="""
            hello
        world！
        Welcome to my party guys!""",
        size_hint_x=1))
        m = ModalView(auto_dismiss=True, size_hint=(0.5, 0.5))
        m.add_widget(Label(text="do hesuan"))
        r.add_widget(Button(on_release=lambda *args: m.open()))
        return r


MyApp().run()