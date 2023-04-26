from kivy.app import App
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix import *
from kivy.core.window import Window

class MyApp(App):
    def build(self):
        s = DropDown(size=Window.size)
        s.add_widget(Label(text="hello", size_hint=(1, None)))
        s.add_widget(Label(text="hello2", size_hint=(1, None)))
        return s

MyApp().run()