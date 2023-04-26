from kivy.app import App
from kivy.core.window import Window
import cProfile
Window.size = (800, 100)

class MyApp(App):
    def on_start(self):
        self.icon = '/Users/chengmin/code/PycharmProjects/code/kivy_A06154/resource/graphics/sysicon.png'
        print([i for i in filter(lambda m: not m.startswith('_'), dir(Window))])
        self.profile = cProfile.Profile()
        self.profile.enable()
    def on_stop(self):
        self.profile.disable()
        self.profile.dump_stats('myapp.profile')
    pass

MyApp().run()