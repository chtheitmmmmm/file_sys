from ..SuperTabPanel import *
from kivy.uix.boxlayout import *
from kivy.uix.button import Button, ButtonBehavior
from kivy.properties import *
from kivy.uix.relativelayout import *
from kivy.graphics import *
from kivy.uix.label import *
from kivy.clock import Clock

class BasePanel(SuperTabPanelBehavoir, BoxLayout):
    pass

class BasePanelHeaders(SuperTabPanelHeadersBehavior, RelativeLayout):
    def on_size(self, *args):
        self.canvas.ask_update()

class BasePanelHeader(SuperTabPanelHeaderBehavior, ButtonBehavior, Label):
    default = BooleanProperty(False)
    def on_size(self, *args):
        self.canvas.ask_update()
    def _do_select(self):
        super(BasePanelHeader, self)._do_select()
        with self.canvas.before:
            Color(18 / 255, 46 / 255, 254 / 255)
            Rectangle(pos=self.pos, size=self.size)

    def _do_unselect(self):
        super(BasePanelHeader, self)._do_unselect()
        with self.canvas.before:
            Color(68 / 255, 86 / 255, 255 / 255)
            Rectangle(pos=self.pos, size=self.size)

    def _do_press(self):
        super(BasePanelHeader, self)._do_release()
        self.dispatch("on_select")

    def on_kv_post(self, base_widget):
        super(BasePanelHeader, self).on_kv_post(base_widget)
        if self.default:
            self.selected = True
            Clock.schedule_once(lambda v: self.parent.parent.dispatch("on_switch", self))

class BasePanelContent(SuperTabPanelContentBehavior, RelativeLayout):
    pass

class BasePanelView(SuperTabPanelViewBehavoir, RelativeLayout):
    pass

__all__ = ("BasePanel", "BasePanelView", "BasePanelHeader",
           "BasePanelContent", "BasePanelHeaders")