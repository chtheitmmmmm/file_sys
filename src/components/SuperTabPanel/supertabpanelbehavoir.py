from kivy.uix.widget import Widget
from kivy.properties import *
from statemachine_decorator import state_define
from kivy.clock import Clock

class SuperTabPanelBehavoir(object):
    """
    布局完全由你自己决定！
    你只需要将一个 SuperTabPanelHeadersBehavior 和一个 SuperTabPanelViewBehavoir
    对象作为本元素子类，你可以自定义触发 on_select 事件的方式
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type("on_switch")
        self.__headers = None
        self.__view = None

    def __get_header(self):
        return self.__headers

    def __set_header(self, h):
        if not isinstance(h, SuperTabPanelHeadersBehavior):
            raise Exception("Headers must be isinstance SuperTabPanelHeadersBehavior!")
        else:
            self.__headers = h
            return True

    def __get_view(self):
        return self.__view

    def __set_view(self, v):
        if not isinstance(v, SuperTabPanelViewBehavoir):
            raise Exception("View must be isinstance SuperTabPanelViewBehavoir!")
        else:
            self.__view = v
            return True

    headers = AliasProperty(__get_header, __set_header)
    view = AliasProperty(__get_view, __set_view)

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        assert len(self.children) == 2 and any(isinstance(h, SuperTabPanelHeadersBehavior) for h in self.children) and any(isinstance(v, SuperTabPanelViewBehavoir) for v in self.children), "A headers and a view are expected as children!"
        for child in self.children:
            if isinstance(child, SuperTabPanelHeadersBehavior):
                self.headers = child
            elif isinstance(child, SuperTabPanelViewBehavoir):
                self.view = child

    def on_switch(self, header):
        assert isinstance(header, SuperTabPanelHeaderBehavior)
        if not self.view:
            for child in self.children:
                if isinstance(child, SuperTabPanelHeadersBehavior):
                    self.headers = child
                elif isinstance(child, SuperTabPanelViewBehavoir):
                    self.view = child
        self.view.switch_to(header)


class SuperTabPanelHeadersBehavior(object):
    """Header区，子元素应为 SuperTabPanelHeaderBehavior"""
    def on_kv_post(self, base_widget):
        super(SuperTabPanelHeadersBehavior, self).on_kv_post(base_widget)
        assert all(isinstance(w, SuperTabPanelHeaderBehavior) for w in self.children), "Children of SUperTabPanelHeaders must all be SuperTabPanelHeaderBehavior"



class SuperTabPanelHeaderBehavior(object):
    """关联了一个子元素（类型为 SuperTabPanelContentBehavior），但该元素仅用于 SuperTabPanelBehavoir 切换，不一定渲染"""
    def __init__(self, **kwargs):
        super(SuperTabPanelHeaderBehavior, self).__init__(**kwargs)
        self.selected = False
        self.register_event_type("on_select")
        self.register_event_type("on_unselect")

    def on_kv_post(self, base_widget):
        super(SuperTabPanelHeaderBehavior, self).on_kv_post(base_widget)
        if not len(self.children) == 1 or not isinstance(self.children[0], SuperTabPanelContentBehavior):
            raise Exception("Must relate to a SuperTabPanelContentBehavior's object!!")
        assert isinstance(self.parent, SuperTabPanelHeadersBehavior)
        self.__content = self.children[0]
        self.clear_widgets()

    def _do_select(self):
        for header in self.parent.children:
            if header is not self:
                header.dispatch("on_unselect")
        self.parent.parent.dispatch("on_switch", self)

    def _do_unselect(self):
        pass

    def on_select(self):
        if not self.selected:
            self.selected = True
            self._do_select()

    def on_unselect(self):
        if self.selected:
            self.selected = False
            self._do_unselect()

    @property
    def content(self):
        return self.__content

class SuperTabPanelContentBehavior(object):
    """子元素，用于与 SuperTabPanelHeaderBehavior 关联"""
    def on_kv_post(self, base_widget):
        super(SuperTabPanelContentBehavior, self).on_kv_post(base_widget)
        assert isinstance(self.parent, SuperTabPanelHeaderBehavior), f"Content {self} can noly be son fo Header."


class SuperTabPanelViewBehavoir(object):
    """其 canvas 用于显示被选中的 Header 的 _content 元素的区域"""
    def on_kv_post(self, base_widget):
        super(SuperTabPanelViewBehavoir, self).on_kv_post(base_widget)
        assert len(self.children) == 0, "View's child was controled by panel."

    def switch_to(self, header):
        assert isinstance(header, SuperTabPanelHeaderBehavior)
        try:
            self.remove_widget(self.children[0])
        except IndexError:
            pass
        self.add_widget(header.content)

__all__ = ("SuperTabPanelBehavoir", "SuperTabPanelHeadersBehavior",
           "SuperTabPanelHeaderBehavior", "SuperTabPanelContentBehavior",
           "SuperTabPanelViewBehavoir")