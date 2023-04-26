from kivy.uix.modalview import ModalView
from promise.promise import Promise
from kivy.properties import *
import  sysapp

class EncryptSetting(ModalView):
    file = ObjectProperty(None)
    group = StringProperty("encrypt_strategy")
    def __init__(self, **kwargs):
        super(EncryptSetting, self).__init__(**kwargs)
        self.register_event_type("on_confirm")
        self.register_event_type("on_cancel")

    def on_confirm(self):
        loading =  sysapp.sysapp.show_loading_toast("解密中" if self.file.is_encrypted else "加密中")
        Promise().resolve(None) \
            .then(lambda v: self._encrypt(self.file)) \
            .then(lambda v: loading.dismiss(), lambda v: loading.dismiss()) \
            .then(lambda v:  sysapp.sysapp.show_success_toast("解密成功" if not self.file.is_encrypted else "加密成功")) \
            .then(lambda v:  sysapp.sysapp.logger.dispatch("on_encrypt", self.file)) \
            .catch(lambda e:  sysapp.sysapp.show_error_toast(str(e)))\
            .then(lambda v: self.dismiss())

    def on_cancel(self):
        self.dismiss()

    def _encrypt(self, file):
        nf = self.file.convert
        self.file = nf