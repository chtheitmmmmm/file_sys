from .....fileinfopages.filesviewpage.fileitemspage.fileitems import FileItems
import  sysapp

class SendFileItems(FileItems):
    def generate_data(self):
        return  sysapp.sysapp.user.sends

__all__ = ("SendFileItems",)