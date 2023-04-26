from kivy.uix.screenmanager import *
from kivy.properties import *
from .fileviewpage import FileViewPage
from .fileitemspage import FileItemsPage
import  sysapp

class FilesViewPage(ScreenManager):

    def on_kv_post(self, base_widget):
        super(FilesViewPage, self).on_kv_post(base_widget)
        self.register_event_type('on_back')
        self.register_event_type("on_view")

    def on_view(self, file):
        self.get_screen('view').file = file
        self.transition.direction = "left"
        self.current = "view"
        sysapp.sysapp.logger.dispatch("on_read", file)

    def on_back(self):
        self.transition.direction = "right"
        self.current = "items"
        self.current_screen.dispatch("on_refresh")

__all__ = ("FilesViewPage",)