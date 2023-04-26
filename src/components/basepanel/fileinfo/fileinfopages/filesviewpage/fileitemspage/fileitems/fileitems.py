from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.properties import *
from pathlib import Path
from .fileitem import FileItem

class FileItems(ScrollView):
    files = ListProperty([])

    def on_kv_post(self, base_widget):
        super(FileItems, self).on_kv_post(base_widget)
        self.ctn = BoxLayout(orientation="vertical")
        self.add_widget(self.ctn)
        self.refresh()
        self.register_event_type("on_view")
        self.register_event_type("on_refresh")

    def on_files(self, *args):
        self.ctn.clear_widgets()
        for f in self.files:
            self.ctn.add_widget(FileItem(file=f, size_hint_y=100 / (self.ctn.size[1] if self.ctn.size[1] else 100)))
        self.ctn.size_hint_y = (100 * len(self.ctn.children)) / (1200 - 180)
        self.scroll_to(self.ctn)

    def on_view(self, file):
        self.parent.dispatch('on_view', file)

    def generate_data(self):
        return []

    def refresh(self):
        """刷新数据"""
        self.files = self.generate_data()

    def on_refresh(self):
        self.refresh()


__all__ = ("FileItems", )