from ...fileinfopages.filesviewpage import FilesViewPage
from promise.promise import Promise
import  sysapp

class RecieveFilesViewPage(FilesViewPage):
    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.register_event_type('on_delete')

    def on_delete(self, file):
        Promise().resolve(file)\
            .then(lambda f: self._delete(f))\
            .then(lambda v:  sysapp.sysapp.show_success_toast("删除成功"))\
            .catch(lambda e:  sysapp.sysapp.show_error_toast(str(e)))


    def _delete(self, file):
         sysapp.sysapp.user.del_file(file)
         sysapp.sysapp.user.del_file(file.sig_path)
         self.dispatch("on_back")

__all__ = ("RecieveFilesViewPage",)