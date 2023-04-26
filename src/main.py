import tkinter
t = tkinter.Tk()
t.withdraw()
import kivy
kivy.require('2.1.0')
from kivy.config import Config
Config.read('config.ini')

from sysapp import sysapp
sysapp.run()