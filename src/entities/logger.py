import csv
from datetime import datetime
from kivy.event import EventDispatcher
from kivy.properties import *

class Logger(EventDispatcher):
    """
    写记录审计
    """
    operator = ObjectProperty(None)

    def __init__(self,*, master_user, **kwargs):
        super(Logger, self).__init__(**kwargs)
        self.operator = master_user
        p = "database/logs.csv"
        self.stream = csv.DictWriter(
            open(p, 'a', encoding='utf-8'),
            fieldnames=csv.DictReader(
                open(p, encoding='utf-8')
            ).fieldnames)
        self.register_event_type("on_read")
        self.register_event_type("on_send")
        self.register_event_type("on_encrypt")
        self.register_event_type("on_delete")
        self.register_event_type("on_print")

    def _get_time_str(self):
        return datetime.now().strftime('%Y.%m.%d %H:%M:%S')

    def on_read(self, file):
        self.stream.writerow({
            'time': self._get_time_str(),
            'operator': self.operator.name,
            'operate': "查看",
            'filename': file.name,
            'relate': file.master.name
        })

    def on_send(self, file, reciever):
        self.stream.writerow({
            'time': self._get_time_str(),
            'operator': self.operator.name,
            'operate': "发送",
            'filename': file.name,
            'relate': reciever.name
        })

    def on_encrypt(self, file):
        self.stream.writerow({
            'time': self._get_time_str(),
            'operator': self.operator.name,
            'operate': "解密" if file.is_encrypted else '加密',
            'filename': file.name,
            'relate': self.operator.name
        })

    def on_delete(self, file):
        self.stream.writerow({
            'time': self._get_time_str(),
            'operator': self.operator.name,
            'operate': "删除",
            'filename': file.name,
            'relate': file.master.name
        })

    def on_print(self, file):
        self.stream.writerow({
            'time': self._get_time_str(),
            'operator': self.operator.name,
            'operate': "打印",
            'filename': file.name,
            'relate': file.master.name
        })

__all__ = ("Logger",)