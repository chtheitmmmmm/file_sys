from ..toast import Toast
from kivy.animation import *
from kivy.uix.image import Image
from kivy.properties import *

class LoadingImage(Image):
    angle = NumericProperty(0)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        angle = 360
        anim = Animation(angle=angle)

        def r(*args):
            nonlocal angle, anim, self
            angle += 360
            anim = Animation(angle=angle, transition=AnimationTransition().in_back)
            anim.on_complete = r
            anim.start(self)

        anim.on_complete = r
        anim.start(self)

class LoadingToast(Toast):
    pass

__all__ = ("LoadingToast","LoadingImage")