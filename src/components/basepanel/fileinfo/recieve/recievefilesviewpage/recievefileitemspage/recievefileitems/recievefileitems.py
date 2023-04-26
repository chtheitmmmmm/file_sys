from .....fileinfopages.filesviewpage.fileitemspage.fileitems import FileItems
import  sysapp
class RecieveFileItems(FileItems):
    def generate_data(self):
        return  sysapp.sysapp.user.receives