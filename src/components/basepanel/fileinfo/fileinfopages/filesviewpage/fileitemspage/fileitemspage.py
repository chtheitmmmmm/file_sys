from kivy.uix.screenmanager import *
from kivy.uix.boxlayout import *

class FileItemsPageLayuot(BoxLayout):

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.register_event_type('on_view')
        self.register_event_type("on_refresh")

    def on_view(self, file):
        self.parent.dispatch("on_view", file)

    def on_refresh(self):
        self.children[-1].dispatch("on_refresh")

class FileItemsPage(Screen):

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.register_event_type('on_view')
        self.register_event_type("on_refresh")

    def on_view(self, file):
        self.parent.dispatch("on_view", file)

    def on_refresh(self):
        self.children[0].dispatch("on_refresh")


__all__ = ("FileItemsPage", "FileItemsPageLayuot")