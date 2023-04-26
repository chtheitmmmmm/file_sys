from kivy.uix.relativelayout import *
from ....SuperTabPanel import *

class FileInfoPages(SuperTabPanelContentBehavior, RelativeLayout):
    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.register_event_type('on_show')

    def on_show(self):
        self.children[0].get_screen('items').dispatch("on_refresh")

__all__ = ("FileInfoPages",)