from kivy.app import App
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.graphics import Rotate
from kivy.animation import Animation, AnimationTransition
from kivy.properties import NumericProperty

Builder.load_string('''                                                                                                                                        
<Loading>:                                                                                                                                                 
    canvas.before:                                                                                                                                             
        PushMatrix                                                                                                                                             
        Rotate:                                                                                                                                                
            angle: self.angle                                                                                                                                  
            axis: (0, 0, 1)                                                                                                                                    
            origin: self.center                                                                                                                                
    canvas.after:                                                                                                                                              
        PopMatrix     
    source: "/Users/chengmin/code/PycharmProjects/code/kivy_A06154/resource/graphics/loading.png"                                                                                                                                      
''')

class Loading(Image):
    angle = NumericProperty(0)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        angle = 360
        anim = Animation(angle=angle)
        def r(*args):
            nonlocal angle, anim, self
            angle += 360
            anim = Animation(angle = angle, transition=AnimationTransition().linear)
            anim.on_complete = r

            anim.start(self)

        anim.on_complete = r
        anim.start(self)


class TestApp(App):
    def build(self):
        return Loading()

TestApp().run()