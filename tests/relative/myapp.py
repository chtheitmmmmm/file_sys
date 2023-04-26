from kivy.app import App
from kivy.core.window import Window
import cProfile
print(Window.size)

class MyApp(App):
    def on_start(self):
        print(Window.size)

    pass

MyApp().run()