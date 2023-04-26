from ....fileinfopages.filesviewpage.fileviewpage import *
from promise.promise import Promise

class RecieveFileViewPage(FileViewPage):
    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.register_event_type('on_delete')

    def on_delete(self, file):
        self.parent.dispatch('on_delete', file)

class RecieveFileViewPageLayout(FileViewPageLayout):
    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.register_event_type('on_delete')

    def on_delete(self, file):
        self.parent.dispatch('on_delete', file)

__all__ = ("RecieveFileViewPage", "RecieveFileViewPageLayout")
