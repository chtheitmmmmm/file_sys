from .....fileinfopages.filesviewpage.fileitemspage.fileitems import FileItems
from  entities.user import User
import  sysapp

class PlazaFileItems(FileItems):
    def generate_data(self):
        return User.unencrypteds()

__all__ = ("PlazaFileItems",)