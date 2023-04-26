from kivy.uix.modalview import ModalView
from kivy.properties import *

class Toast(ModalView):
    """The base class of toast"""
    msg = StringProperty('')

__all__ = ("Toast",)