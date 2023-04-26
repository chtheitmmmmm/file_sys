from ..useritem import UserItem
import  sysapp
from time import time
from .....superbutton import SuperButton
from kivy.clock import Clock
class FrozenButton(SuperButton):
    def on_touch_down(self, touch):
        if touch.is_mouse_scrolling:
            return False
        if not self.collide_point(touch.x, touch.y - self.parent.parent.parent.parent.parent.g_translate.xy[1]):
            return False
        if self in touch.ud:
            return False
        touch.grab(self)
        touch.ud[self] = True
        self.last_touch = touch
        self.__touch_time = time()
        self._do_press()
        print(self.parent.master_user.name)
        self.dispatch('on_press')
        return True

    def on_touch_up(self, touch):
        if touch.grab_current is not self:
            return super().on_touch_up(touch)
        assert(self in touch.ud)
        touch.ungrab(self)
        self.last_touch = touch

        if (not self.always_release and
                not self.collide_point(touch.x, touch.y - self.parent.parent.parent.parent.parent.g_translate.xy[1])):
            self._do_release()
            return

        touchtime = time() - self.__touch_time
        if touchtime < self.min_state_time:
            self.__state_event = Clock.schedule_once(
                self._do_release, self.min_state_time - touchtime)
        else:
            self._do_release()
        self.dispatch('on_release')
        return True

class UserItemFrozenable(UserItem):
    def frozen_user(self):
         sysapp.sysapp.users.frozen(self.master_user)
         self.parent.parent.parent.parent.dispatch("on_refresh")

__all__ = ("UserItemFrozenable", "FrozenButton")