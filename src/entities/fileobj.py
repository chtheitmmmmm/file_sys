from pathlib import Path, WindowsPath, PosixPath
import os
from datetime import datetime
from Crypto.Cipher import DES
from Crypto.Hash import MD5
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
import  sysapp
from chardet.universaldetector import UniversalDetector

class PathObj(Path):
    def __new__(cls, *args, **kwargs):
        if cls is PathObj:
            cls = WindowsPathObj if os.name == 'nt' else PosixPathObj
        return Path.__new__(cls, *args, **kwargs)

    @property
    def children(self):
        return [f for f in self.iterdir()]

    def child(self, name):
        """ 返回目录下的某一个文件路径 """
        return type(self)(str(self) + "/" + name)

class WindowsPathObj(PathObj, WindowsPath):
    pass

class PosixPathObj(PathObj, PosixPath):
    pass

class FileObj(PathObj):
    """表示用户的文件，可以是上传的、发送的（接收的）"""
    def __new__(cls, *args, **kwargs):
        if cls is FileObj:
            cls = WindowsFileObj if os.name == 'nt' else PosixFileObj
        return PathObj.__new__(cls, *args, **kwargs)

    @property
    def extension(self):
        return self.name.split('.')[-1]

    @property
    def without_extension(self):
        return self.name.split('.')[-2]

    @property
    def e_name(self):
        return self.without_extension + ".e"

    @property
    def e_path(self):
        return self.parent.child(self.e_name)

    @property
    def is_encrypted(self):
        """文件对象是否加密"""
        return self.extension == 'e'

    @property
    def create_time(self):
        """创建的时间"""
        return datetime.fromtimestamp(self.stat().st_ctime).strftime("%Y.%m.%d")

    @property
    def watermask_name(self):
        return ''

class WindowsFileObj(FileObj, WindowsPathObj):
    pass

class PosixFileObj(FileObj, PosixPathObj):
    pass

class UserFileObj(FileObj):
    """用户上传的文件"""

    def __new__(cls, *args, **kwargs):
        if cls is UserFileObj:
            cls = WindowsUserFileObj if os.name == 'nt' else PosixUserFileObj
        return PathObj.__new__(cls, *args, **kwargs)

    @property
    def txt_name(self):
        return self.without_extension + ".txt"

    @property
    def txt_path(self):
        return self.parent.child(self.txt_name)

    @property
    def content(self):
        ctt = self.read_bytes()
        det = UniversalDetector()
        det.feed(ctt)
        return ctt.decode(det.result['encoding'] if det.result['confidence'] > 0.8 else 'utf-8')

    @property
    def master(self):
        return  sysapp.sysapp.users[self.parent.name] if self.parent.name != 'file' else  sysapp.sysapp.users[self.parent.parent.name]

    @property
    def watermask_name(self):
        return self.master.name

class WindowsUserFileObj(UserFileObj, WindowsFileObj):
    pass

class PosixUserFileObj(UserFileObj, PosixFileObj):
    pass

class MasterFileObj(UserFileObj):
    """主用户的文件对象，可以转换自身加密性"""

    def __new__(cls, *args, **kwargs):
        if cls is MasterFileObj:
            cls = WindowsMasterFileObj if os.name == 'nt' else PosixMasterFileObj
        return PathObj.__new__(cls, *args, **kwargs)

    @property
    def master(self):
        """返回文件对象的作者 或 发送者"""
        return  sysapp.sysapp.users[self.parent.parent.name]

    @property
    def watermask_name(self):
        return self.master.name

    @property
    def convert(self):
        """
        返回自身的转换，若自身为加密状态，则转换为非加密状态
        请必须在函数外手动重新赋值 self
        """
        if self.is_encrypted:
            ctt = bytearray(self.read_bytes())
            assert len(ctt) % 8 == 1, "Encrypted file is broken."
            fill = ctt.pop()
            ctt = bytearray(DES.new(
                self.master.des_key,
                DES.MODE_ECB
            ).decrypt(ctt))
            for i in range(1, fill + 1):
                assert ctt[-i] == fill, "Encrypted file is broken."
            for i in range(fill):
                ctt.pop()
            self.write_bytes(ctt)
            return self.rename(self.txt_path)
        else:
            ctt = bytearray(self.read_bytes())
            fill = (8 - len(ctt) % 8) if len(ctt) % 8 else 0
            for i in range(fill):
                ctt.append(fill)
            ctt = bytearray(DES.new(
                    self.master.des_key,
                    DES.MODE_ECB
                ).encrypt(ctt))
            ctt.append(fill)
            self.write_bytes(ctt)
            return self.rename(self.e_path)


    @property
    def content(self):
        if self.is_encrypted:
            ctt = bytearray(self.read_bytes())
            assert len(ctt) % 8 == 1, "Encrypted file is broken."
            fill = ctt.pop()
            ctt = bytearray(DES.new(
                self.master.des_key,
                DES.MODE_ECB
            ).decrypt(ctt))
            for i in range(1, fill + 1):
                assert ctt[-i] == fill, "Encrypted file is broken."

            for i in range(fill):
                ctt.pop()
            return ctt.decode('utf-8')
        else:
            return self.read_text('utf-8')

class WindowsMasterFileObj(MasterFileObj, WindowsUserFileObj):
    pass

class PosixMasterFileObj(MasterFileObj, PosixUserFileObj):
    pass

class RecieveFileObj(FileObj):
    """从他人那里接收来的文件的对象"""

    def __new__(cls, *args, **kwargs):
        if cls is RecieveFileObj:
            cls = WindowsRecieveFileObj if os.name == 'nt' else PosixRecieveFileObj
        return PathObj.__new__(cls, *args, **kwargs)

    @property
    def master(self):
        """返回文件对象的作者--或者说--发送者"""
        return  sysapp.sysapp.users[self.parent.name]

    @property
    def watermask_name(self):
        return self.master.name

    @property
    def sig_name(self):
        return self.without_extension + ".sig"

    @property
    def sig_path(self):
        return self.parent.child(self.sig_name)

    @property
    def content(self):
        sender = self.master
        # 检查 .sig 文件是否存在
        if not self.sig_path.exists():
            raise FileNotFoundError("签名文件丢失")
        try:
            pkcs1_15.new(sender.public_key)\
            .verify(
                MD5.new(self.read_bytes()),
                self.sig_path.read_bytes()
            )
        except ValueError:
            raise Exception("验证签名失败")
        deskey =  DES.new(sender.des_key, DES.MODE_ECB)
        ctt = bytearray(self.read_bytes())
        fill = ctt.pop()
        ctt = bytearray(deskey.decrypt(ctt))
        for i in range(1, fill + 1):
            assert ctt.pop() == fill, "源文件已损坏"
        det = UniversalDetector()
        det.feed(ctt)
        return ctt.decode(det.result['encoding'] if det.result['confidence'] > 0.8 else 'utf-8')

    @property
    def sender(self):
        return  sysapp.sysapp.users[self.parent.parent.parent.name]

class WindowsRecieveFileObj(RecieveFileObj, WindowsFileObj):
    pass

class PosixRecieveFileObj(RecieveFileObj, PosixFileObj):
    pass

__all__ = ('PathObj', 'FileObj', 'UserFileObj', 'MasterFileObj', 'RecieveFileObj')