from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.properties import *
from .useritemfrozenable import UserItemFrozenable
from .useritem import UserItem
import  sysapp, math
from ....basepanel import *

class UserItems(BasePanelContent, ScrollView):

    def on_kv_post(self, base_widget):
        super(UserItems, self).on_kv_post(base_widget)
        self.ctn = BoxLayout(size_hint=(1, 1), orientation="vertical")
        self.add_widget(self.ctn)
        self.register_event_type("on_refresh")
        self.dispatch("on_refresh")
        self.scroll_to(self.ctn)

    def on_refresh(self):
        self.ctn.clear_widgets()
        user_item_outer_ctn = None
        for index, (user_id, user) in enumerate( sysapp.sysapp.users.items()):
            if not index & 1:
                user_item_outer_ctn = RelativeLayout(size_hint_y = 600 / self.ctn.size[1] if self.ctn.size[1] else 600)
                self.ctn.add_widget(user_item_outer_ctn)
                user_item_inner_ctn = RelativeLayout(size_hint=(0.5, 1), pos_hint={"x": 0, "y": 0})
            else:
                user_item_inner_ctn = RelativeLayout(size_hint=(0.5, 1), pos_hint={"x": 0.5, "y": 0})
            user_item_outer_ctn.add_widget(user_item_inner_ctn)
            if  sysapp.sysapp.user.type == "超级管理员" and user.type != "超级管理员":
                user_item_inner_ctn.add_widget(UserItemFrozenable(master_user=user, size_hint=(0.7, 0.55), pos_hint = {"x": 0.15, "y": 0.225}))
            else:
                user_item_inner_ctn.add_widget(UserItem(master_user=user, size_hint=(0.7, 0.55), pos_hint = {"x": 0.15, "y": 0.225}))
        self.ctn.size_hint_y = len(self.ctn.children) * 600 / 1200



__all__ = ("UserItems",)