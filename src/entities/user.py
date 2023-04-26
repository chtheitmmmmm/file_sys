"""
用户类，当用户成功登入时，从数据库中获取用户的发送、接收消息
"""
import shelve, os, tkinter.filedialog
from tkinter.filedialog import askopenfilename
from tkinter import Tk
from kivy.properties import *
from pathlib import Path
from Crypto.Cipher import DES   # DES 对称加密算法
from Crypto.Hash import MD5     # MD5 哈希算法
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA# 非对称加密签名
from Crypto import Random
from .fileobj import *
import  sysapp


class User:
    """
        用户对象
        -- 用户名 id: str
        -- 密码 password: str
        -- 姓名 name: str
        -- 单位 department: "研发部" | "推广部" | "工程部" | "管理部"
        -- 类型 type: "cmn" | "mng" | "smng" ===>>> 用户 | 管理员 | 超级管理员
        -- 状态 state: "frozen" | "plain" ===>>> 被删除（超级管理员） | 没有被删除
    """

    type = "用户"
    def __init__(self, info):
        """
        :param info: 从 users.db 中获取到的 value
        """
        self.id = info['id']
        self.password = info['password']
        self.name = info['name']
        self.department = info['department']
        self.state = info['state'] # "frozen | plain"
        self.rootdir = PathObj(f"database/fileroot/{self.id}")

    def __eq__(self, other):
        return other.id == self.id

    def generate_data(self):
        return {
            'department': self.department,
            'id': self.id,
            'name': self.name,
            'password': self.password,
            'state': self.state,
            'type': self.type,
        }

    @staticmethod
    def register(info):
        """
        用户注册，创建用户目录及密钥
        若用户已注册则报错
        """
        match info['type']:
            case '用户':
                user = User(info)
            case '管理员':
                user = Manager(info)
            case '超级管理员':
                user = SuperManager(info)
        user.rootdir.mkdir()
        user.key_root.mkdir()
        user.des_key_path.write_bytes(Random.get_random_bytes(8)) # 创建 .deskey文件
        rsakey = RSA.generate(2048)
        user.public_key_path.write_bytes(rsakey.public_key().export_key())  # 创建 .pub 文件
        user.private_key_path.write_bytes(rsakey.export_key())  # 创建 .pri 文件
        user.file_root.mkdir()      # 创建 file 文件夹
        user.recieve_root.mkdir()   # 创建 recieve 文件夹
        return user

    @property
    def des_key(self):
        """获取用户DES密钥"""
        key = self.des_key_path.read_bytes()
        return key

    @property
    def des_key_path(self):
        return self.key_root.child('.deskey')

    @property
    def public_key(self):
        """获取用户公钥"""
        return RSA.import_key(self.public_key_path.read_bytes())

    @property
    def public_key_path(self):
        return self.key_root.child('.pub')

    @property
    def private_key(self):
        """获取用户私钥"""
        return RSA.import_key(self.private_key_path.read_bytes())

    @property
    def private_key_path(self):
        return self.key_root.child('.pri')

    @property
    def key_root(self):
        return self.rootdir.child('key')

    @property
    def file_root(self):
        return self.rootdir.child('file')

    @property
    def recieve_root(self):
        return self.rootdir.child('recieve')

    @property
    def files(self):
        """获取用户自身发布过的所有文件，返回 list[Path]"""
        return [MasterFileObj(f) for f in self.file_root.children]

    @property
    def receives(self):
        """
        获取用户接收到的所有文件，返回一个列表list[RecieveFileObj("*.e)]
        """
        return [
            RecieveFileObj(file)
            for sender in self.recieve_root.iterdir()
                for file in sender.iterdir()
                    if file.name.endswith(".e")
        ]

    @property
    def sends(self):
        """
        获取用户发送的所有文件，返回列表
        :return: list[RecieveFileObj(
        """
        return [
            f
            for user_root in RecieveFileObj("database/fileroot").iterdir()   # 所有用户
                for sender in user_root.child('recieve').iterdir() # 所有用户接收目录的发送者目录
                    if sender.name == self.id
                        for f in sender.iterdir()
                            if f.is_encrypted # 发送者为本用户
        ]

    @staticmethod
    def unencrypteds():
        """
        获取所有用户没有被加密的文件
        返回列表 list[UserFileObj("*.txt")
        """
        return [
            f
            for user in UserFileObj("database/fileroot").iterdir()
                for f in user.child('file').iterdir()
                    if not f.is_encrypted
        ]

    @staticmethod
    def get_des_key(userid):
        """获取指定 id 用户的 des key"""
        return  sysapp.users[userid].des_key

    @staticmethod
    def get_public_key(userid):
        """获取指定 id 用户的 public key"""
        return  sysapp.users[userid].public_key

    @staticmethod
    def get_private_key(userid):
        """获取指定 id 用户的 private key（这个方法在逻辑上真的存在被调用的可能吗？）"""
        return  sysapp.users[userid].private_key

    @staticmethod
    def get_ones_root(ones: str):
        return UserFileObj(f'database/fileroot/{ones}')

    @staticmethod
    def get_ones_sender(ones: str, sender: str):
        return UserFileObj(f'database/fileroot/{ones}/receive/{sender}')

    def get_file(self, name: str):
        """获取某个文件的 Path 对象"""
        return self.file_root.child(name)

    def get_sender(self, sender_id: str):
        """获取id为 sender_id 的发送者的发送文件目录"""
        return self.recieve_root.child(sender_id)

    # TODO: Add log writing.
    def upload_file(self):
        """
        上传txt文件，
        如果已上传过则报错，
        返回是否上传成功
        """
        f = askopenfilename(filetypes=[("text", ".txt")])
        if f:
            filepath = MasterFileObj(f)
            distfilepath = MasterFileObj(self.get_file(filepath.name))
            try:
                distfilepath.touch(exist_ok=False)
                distfilepath.e_path.touch(exist_ok=False)
            except OSError:
                raise Exception("已上传过同名文件")
            else:
                os.remove(distfilepath.e_path)
            distfilepath.write_bytes(filepath.read_bytes())
            return True
        else:
            return False

    def send_file(self, reciever_id, f: MasterFileObj):
        """
        发送 file 文件给一个用户 reciever
        若发送失败则报错:
            目标用户未注册
            已发送过同名文件
        """
        if f.is_encrypted:
            e = f.read_bytes()
        else:
            key = self.des_key
            e = bytearray(f.read_bytes())
            fill = (8 - len(e) % 8) if len(e) % 8 else 0
            for i in range(fill):
                e.append(fill)
            e = bytearray(DES.new(
                key,
                DES.MODE_ECB
            ).encrypt(e))
            e.append(fill)
        pri = self.private_key
        sig = pkcs1_15.new(pri).sign(MD5.new(e))    # 签名后的数据
        if reciever:= sysapp.sysapp.users.get(reciever_id):
            send_root = reciever.recieve_root.child(self.id)
            send_root.mkdir(exist_ok=True)
            encrypt_file = send_root.child(f.e_name)
            sig_file = send_root.child(f.without_extension + ".sig")
            try:
                encrypt_file.touch(exist_ok=False)
                sig_file.touch(exist_ok=False)
            except FileExistsError:
                raise Exception("已发送过同名文件")
            encrypt_file.write_bytes(e)
            sig_file.write_bytes(sig)
        else:
            raise Exception("目标用户未注册！")

    def del_file(self, f: MasterFileObj):
        """删除文件"""
        if f.exists():
            os.remove(f)
        else:
            raise Exception("要删除的文件不存在！")

    def del_rcv_file(self, f: RecieveFileObj):
        """
        delete recieved file (and its
        :return:
        """
        os.remove(f)
        os.remove(f.sig_path)

class Manager(User):
    type = "管理员"

class SuperManager(User):
    """可以冻结/解冻用户"""
    type = "超级管理员"
    def convert_user(self, user: User):
        if user.state == 'plain':
             sysapp.users.frozen(user)
        else:
             sysapp.users.unfrozen(user)

class Users(dict):
    """管理用户数据库"""
    def __init__(self, db):
        super(Users, self).__init__()
        self.db = shelve.open(db)
        for id_card, info in self.db.items():
            match info['type']:
                case '用户':
                    self[id_card] = User(info)
                case '管理员':
                    self[id_card] = Manager(info)
                case '超级管理员':
                    self[id_card] = SuperManager(info)

    def register(self, info):
        if self.get(info['id']):
            raise Exception("Register_fail")
        user = User.register(info)
        self[info['id']] = user
        self.db[info['id']] = user.generate_data()
        return user

    def frozen(self, user):
        """解冻或冻结用户"""
        self[user.id].state = 'frozen' if self[user.id].state == 'plain' else 'plain'

    def unfrozen(self, user):
        self[user.id].state = 'plain'

    def close(self):
        for id_card, user in self.items():
            self.db[id_card] = user.generate_data()
        self.db.close()

__all__ = ("User", "Manager", "SuperManager", "Users")
