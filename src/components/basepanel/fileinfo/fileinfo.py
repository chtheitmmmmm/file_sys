from ...SuperTabPanel import *
from ...basepanel import *
from kivy.uix.boxlayout import *
from kivy.uix.label import *
from kivy.uix.relativelayout import *
from kivy.graphics import *
from kivy.properties import *
from kivy.uix.button import ButtonBehavior
from kivy.clock import Clock

class FileInfo(SuperTabPanelContentBehavior, SuperTabPanelBehavoir, BoxLayout):
    pass

class FileInfoHeaders(SuperTabPanelHeadersBehavior, BoxLayout):
    pass

class FileInfoHeader(SuperTabPanelHeaderBehavior, ButtonBehavior, Label):
    default = BooleanProperty(False)

    def _do_select(self):
        super()._do_select()
        with self.canvas.before:
            Color(254 / 255, 18 / 255, 18 / 255, 1)
            Rectangle(pos=self.pos, size=self.size)
        self.content.dispatch("on_show")


    def _do_unselect(self):
        super()._do_unselect()
        with self.canvas.before:
            Color(255 / 255, 124 / 255, 124 / 255, 1)
            Rectangle(pos=self.pos, size=self.size)

    def _do_press(self):
        super()._do_release()
        self.dispatch("on_select")

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        if self.default:
            self.selected = True
            Clock.schedule_once(lambda v: self.parent.parent.dispatch("on_switch", self))

class FileInfoView(SuperTabPanelViewBehavoir, RelativeLayout):
    pass

__all__ = ("FileInfo", "FileInfoHeader", "FileInfoHeaders", "FileInfoView")