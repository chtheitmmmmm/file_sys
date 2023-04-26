from .....fileinfopages.filesviewpage.fileitemspage.fileitems import *
import  sysapp

class MyFileItems(FileItems):
    def on_files(self, *args):
        self.ctn.clear_widgets()
        for f in self.files:
            self.ctn.add_widget(FileItem(file=f, size_hint_y=100 / (self.ctn.size[1] if self.ctn.size[1] else 100)))
        self.ctn.size_hint_y = (100 * len(self.ctn.children)) / (1200 - 180 - 120)
        self.scroll_to(self.ctn)

    def generate_data(self):
        """
        传入 app 对象，获取当前用户数据
        :param app:
        :return:
        """
        return  sysapp.sysapp.user.files

__all__ = ("MyFileItems",)
