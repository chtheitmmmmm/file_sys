from ....fileinfopages.filesviewpage.fileviewpage import *
from kivy.uix.modalview import ModalView
from kivy.properties import *
from  entities.fileobj import *
from statemachine_decorator import state_define
from promise.promise import Promise
from .encryptsetting import EncryptSetting
import os,  sysapp

class AskRecieverIdModal(ModalView):
    reciever = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(AskRecieverIdModal, self).__init__(**kwargs)
        self.register_event_type('on_confirm')
        self.register_event_type('on_cancel')

    def on_cancel(self, *args):
        self.dismiss()

    def on_confirm(self, reciever_id):
        pass


class MyFileViewPage(FileViewPage):
    """
    查看文件的page
    有 file 属性
    """


class MyFileViewPageLayout(FileViewPageLayout):

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.register_event_type("on_send")
        self.register_event_type("on_encrypt")
        self.register_event_type("on_delete")

    def on_send(self, file):
        ask = AskRecieverIdModal()
        ask.open()
        ask.on_confirm = \
            lambda reciever_id: \
                Promise.resolve(reciever_id)\
                    .then(lambda i:  sysapp.sysapp.user.send_file(i, file)) \
                    .then(lambda v:  sysapp.sysapp.show_success_toast("发送成功！")) \
                    .then(lambda v: ask.dismiss())\
                    .then(lambda v:  sysapp.sysapp.logger.dispatch('on_send', file,  sysapp.sysapp.users[reciever_id]))\
                    .catch(lambda e:  sysapp.sysapp.show_error_toast(str(e)))\

    def on_encrypt(self, file):
        es = EncryptSetting(file=file)
        es.open()
        on_en = es.on_confirm
        es.on_confirm = lambda : (on_en(), setattr(self, 'file', es.file))


    def on_delete(self, file):
        Promise().resolve(None) \
            .then(lambda v: self._delete(file)) \
            .then(lambda v:  sysapp.sysapp.show_success_toast("删除成功")) \
            .then(lambda v: self.parent.dispatch("on_back"))\
            .then(lambda v:  sysapp.sysapp.logger.dispatch("on_delete", file))\
            .catch(lambda e:  sysapp.sysapp.show_error_toast(str(e)))

    def _delete(self, file):
         sysapp.sysapp.user.del_file(file)


__all__ = ("AskRecieverIdModal", "MyFileViewPage", "MyFileViewPageLayout")