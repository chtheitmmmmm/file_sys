import threading

from kivy.uix.relativelayout import *
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.properties import *
from kivy.clock import Clock
from statemachine_decorator import state_define  # 有限状态机装饰器
import re, shelve, json, requests, validator, promise
import sysapp
from  entities.user import *
from kivy.uix.button import Button

class LoginMsgContent(RelativeLayout):
    pass

class LoginMsg(Popup):
    pass

class ConnectionMsgContent(RelativeLayout):
    pass

class ConnectionMsg(Popup):
    pass

class APICallMsgContent(RelativeLayout):
    pass

class APICallMsg(Popup):
    pass

class RgtMsgContent(RelativeLayout):
    pass

class RgtMsg(Popup):
    pass

# 测试账号，想要测试哪个账号，直接在下方 test 变量中的下标索引中输入相应下标所用即可

tests = [[{
    'id': '210723194905264810',
    'password': '123456'
}, {
    'id': '210723194905264810',
    'password': '123456',
    'confirm_password': '123456',
    'name': '金永阁',
    'department': '管理部',
    'user_type': '超级管理员'
}], [{
    'id': '210723195108294827',
    'password': 'bi0edc',
}, {
    'id': '210723195108294827',
    'password': 'bi0edc',
    'confirm_password': 'bi0edc',
    'name': '徐宝华',
    "department": "研发部",
    'user_type': '管理员'
}]]

test = tests[1]

@state_define({
    "Plain": {"Logining", "Registering"},                       # 普通状态
    "Logining": {"Login_fail", "Logined"},                      # 正在登录
    "Registering": {
        "Register_fail", "API_fail", "Cnt_fail",                # 注册错误
        "Logined"                                               # 注册成功
    },
    "Login_fail": {"Plain"},                                    # 登录失败
    "Register_fail": {"Plain"},                                 # 注册失败
    "API_fail": {"Plain"},                                      # API调用失败
    "Cnt_fail": {"Plain"},                                      # 网络连接失败
    "Logined": None,                                            # 登录成功
}, "Plain")
class LoginScreen(Screen):
    STATE = StringProperty('')
    department = ObjectProperty(None)
    user_type = ObjectProperty(None)    # 用户类型，超级管理员、管理员、用户
    master_user = ObjectProperty(None)  # 当前的用户，登入后设为 CommonUser 类对象

    login_inputs = DictProperty(test[0])                                  # 用户输入的数据，数据绑定
    register_inputs = DictProperty(test[1])
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.bind(STATE=self.onSTATE)
        self.STATE = self.state
        self.register_event_type('on_login')

    def onSTATE(self, instance, value):
        match value:
            case 'Plain':
                pass
            case 'Logining':
                self.login()
            case "Registering":
                self.register()
            case 'Login_fail':
                login_popup = LoginMsg()
                login_popup.on_touch_down = lambda *args: (login_popup.dismiss(), self.switch_state('Plain'))
                login_popup.open()
            case 'API_fail':
                api = APICallMsg()
                api.content.children[0].text = self.data['message']
                api.on_touch_down = lambda *args: (api.dismiss(), self.switch_state('Plain'))
                api.open()
            case 'Cnt_fail':
                con = ConnectionMsg()
                con.on_touch_down = lambda *args: (con.dismiss(), self.switch_state('Plain'))
                con.open()
            case "Register_fail":
                rgf = RgtMsg()
                rgf.on_touch_down = lambda *args: (rgf.dismiss(), self.switch_state("Plain"))
                rgf.open()
            case _:
                print(self.state)

    def login(self):
        """
        登入
        :return:
        """
        ex = Exception()
        promise.Promise().resolve(None)\
            .then(lambda v: self._login())\
            .then(lambda user: self.dispatch("on_login", user))\
            .then(lambda v:  sysapp.sysapp.show_success_toast('登录成功'))\
            .catch(lambda r:  self.switch_state('Login_fail'))


    def _login(self):
        login_validator = validator.Validator(
            self.login_inputs, {
                'id': [lambda i: i in  sysapp.sysapp.users and sysapp.sysapp.users[i].state != 'frozen'],
                'password': [lambda p: self.login_inputs['id'] in  sysapp.sysapp.users and  sysapp.sysapp.users[self.login_inputs['id']].password == p]
            })
        if not login_validator.validate():
            raise
        else:
            return sysapp.sysapp.users[self.login_inputs['id']]

    def on_login(self, user):
        self.parent.dispatch('on_login', user)

    def switch_state(self, state):
        self.switch(state)
        self.STATE = self.state

    def register(self):
        """
        注册
        :return:
        """
        if self.state == 'Registering':
            loading =  sysapp.sysapp.show_loading_toast('注册中')
            r = None
            promise.Promise().resolve(None)\
                .then(lambda v: self._register())\
                .then(lambda user: self.dispatch("on_login", user))\
                .then(lambda v:  sysapp.sysapp.show_success_toast('注册成功')) \
                .catch(lambda s: self.switch_state(str(s))) \
                .catch(lambda r: sysapp.sysapp.show_error_toast(f"注册失败，报错如下\n{r}")) \
                .then(lambda v: loading.dismiss())

    def _register(self):
        """
        输入正确性检验
        """
        register_validator = validator.Validator(
            self.register_inputs, {
                'id': [lambda i: bool(re.compile(r"(^([1-6][1-9]|50)\d{4}(18|19|20)\d{2}((0[1-9])|10|11|12)(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$)|(^([1-6][1-9]|50)\d{4}\d{2}((0[1-9])|10|11|12)(([0-2][1-9])|10|20|30|31)\d{3}$)").findall(i)),
                       lambda i:  sysapp.sysapp.users is not None and not  sysapp.sysapp.users.get(i)],   # 身份证合法
                'name': [lambda n: bool(re.compile(r"^([\u4e00-\u9fa5]{1,20})$").findall(n))], # 姓名合法
                'department': [lambda d: d in ["研发部" , "推广部" , "工程部" , "管理部"]],
                'user_type': [lambda u: u in ["超级管理员", "管理员", "用户"]],
                'password': [lambda p: bool(re.compile(r"^[a-zA-Z0-9]{5,32}$").findall(p))],  # 密码合法
                'confirm_password': [lambda c: c == self.register_inputs['password']]
            })
        if not register_validator.validate():
            raise Exception("Register_fail")
        else:
            # 调用阿里云身份认证接口
            debug = True   # debug 设为 True，则不会调用接口，直接注册
            try:
                if not debug:
                    data = json.loads(requests.request(
                        method="POST",
                        url='https://eid.shumaidata.com/eid/check',
                        params={
                            'idcard': self.register_inputs["id"],
                            'name': self.register_inputs["name"]
                        },
                        headers={
                            'Authorization': 'APPCODE cf531c4214de4801ba1a3efe0e1d7435'
                        },
                    ).content.decode('utf-8'))
                    print(data)
                    if data['code'] != '0':
                        self.data = data    # 供主线程使用
                        raise Exception('API_fail')
                    else:
                        if data['result']['res'] != '1':
                            self.data = {
                                'message': data['result']['description']
                            }
                            raise Exception('API_fail')
                        return  sysapp.sysapp.users.register({
                            'id': self.register_inputs['id'],
                            'password': self.register_inputs['password'],
                            'name': self.register_inputs['name'],
                            'department': self.register_inputs['department'],
                            'type': self.register_inputs['user_type'],
                            'state': 'plain'
                        })
                else:
                    return  sysapp.sysapp.users.register({
                        'id': self.register_inputs['id'],
                        'password': self.register_inputs['password'],
                        'name': self.register_inputs['name'],
                        'department': self.register_inputs['department'],
                        'type': self.register_inputs['user_type'],
                        'state': 'plain',
                    })
            except requests.exceptions.ConnectionError as e:
                # 出现连接错误
                raise Exception('Cnt_fail')

__all__ = ("LoginMsgContent", "LoginMsg",
           "ConnectionMsgContent", "ConnectionMsg",
           "APICallMsgContent", "APICallMsg",
           "RgtMsgContent", "RgtMsg", "LoginScreen")
