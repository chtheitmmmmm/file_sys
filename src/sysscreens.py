from kivy.uix.screenmanager import ScreenManager
import sysapp as sysapp
from  components.userscreen import UserScreen
from  components.managerscreen import ManagerScreen

class SysScreens(ScreenManager):
    def __init__(self, **kwargs):
        super(SysScreens, self).__init__(**kwargs)
        self.register_event_type("on_login")

    def on_login(self, user):
        sysapp.sysapp.user = user
        match user.type:
            case "用户":
                self.add_widget(UserScreen(name='user'))
                self.current = 'user'
            case _:
                self.add_widget(ManagerScreen(name='manager'))
                self.current = 'manager'
        sysapp.sysapp.logger.operator = user

    def on_kv_post(self, base_widget):
        self.current = "login"
        self.current_screen.department.dismiss()
        self.current_screen.user_type.dismiss()
        # self.on_login( sysapp.sysapp.users['421182200304260430'])
