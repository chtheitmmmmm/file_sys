from kivy.properties import *
from kivy.uix.pagelayout import *
from pathlib import Path
from tkinter.filedialog import askopenfilename
from promise import Promise
from statemachine_decorator import state_define
from ..fileinfopages import FileInfoPages
from ....SuperTabPanel import *
import  sysapp

@state_define({
    "plain": {"uploading"}, # 正常状态
    "uploading": {"plain"}, # 正在上传文件
}, "plain")
class Mine(FileInfoPages):
    STATE = StringProperty('')

    def switch_state(self, s):
        self.switch(s)
        self.STATE = self.state

    def upload_file(self):
        self.switch_state('uploading')
        f = Path(askopenfilename(title="选择要上传的 .txt 文件", filetypes=[("text", "*.txt")]))
        Promise().resolve(f)\
            .then(self._upload_file)\
            .then(lambda v: self.switch_state('plain'))

    def _upload_file(self, f: Path): # 异步调用
        filedir = Path(f"database/fileroot/{ sysapp.sysapp.user.id}/fileroot/{f.name}")
        with filedir.open('w') as file:
            file.write(f.read_text(encoding='utf-8'))


__all__ = ("Mine",)