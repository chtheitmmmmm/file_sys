from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.switch import Switch
from ........superbutton.superbutton import SuperButton
from tkinter.filedialog import asksaveasfilename
from promise.promise import Promise
from kivy.properties import *
import time, os
from PIL import Image, ImageDraw, ImageFont
from kivy.uix.image import Image as Img
import  sysapp

class PrintSetting(ModalView):
    """
    打印设置
    """
    fsize = StringProperty('100')
    ang = StringProperty('45')
    lgap = StringProperty('100')
    cgap = StringProperty('100')
    opc = StringProperty('100')
    water = BooleanProperty(True)   # 是否开启水印
    prv = BooleanProperty(True)     # 是否开启预览
    interval = NumericProperty(3)   # 每3秒刷新预览视图
    output_path = StringProperty('')
    file_view = ObjectProperty(None)# 文件视图对象
    disp_width = NumericProperty(275)

    def __init__(self, **kwargs):
        self.register_event_type("on_select_path")
        self.register_event_type("on_refresh_prv")
        self.register_event_type("on_confirm")  # 确定
        self.register_event_type("on_cancel")   # 取消
        self.register_event_type("on_prv_show") # 展示
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        super(PrintSetting, self).on_kv_post(base_widget)
        self.ids.pctn.fields = self.ids.pctn.children[::-1]
        self.ids.wctn.fields = self.ids.wctn.children[::-1]
        prv_ctn = self.ids.prv_ctn
        self.prv_img_widget = PrvImage()
        prv_ctn.add_widget(self.prv_img_widget)
        self.dispatch("on_refresh_prv")

    def on_select_path(self):
        """
        选择路径
        """
        Promise.resolve(None)\
            .then(lambda v: self._select_path())

    def on_water(self, *args):
        if self.water:
            for w in self.ids.wctn.fields:
                if not isinstance(w, Switch):
                    self.ids.wctn.add_widget(w)
        else:
            wctn = self.ids.wctn
            print(wctn.children)
            for field in wctn.fields:
                if not isinstance(field, Switch):
                    wctn.remove_widget(field)
        self.dispatch('on_refresh_prv')

    def on_prv(self, *args):
        if self.prv:
            for w in self.ids.pctn.fields:
                self.ids.pctn.add_widget(w)
        else:
            self.ids.pctn.clear_widgets()

    def on_refresh_prv(self):
        if self.prv:
            temp_fn = ''
            Promise.resolve(None)\
                .then(lambda v: f'___TEMP_{int(time.time())}.png')\
                .then(lambda fn: (self.file_view.export_to_png(fn), temp_fn:=fn))\
                .then(lambda fn: (fn[1], *self._generate_param()))\
                .then(self._generate_prv)\
                .then(self._disp_prv)\
                .catch(lambda e: print('刷新被拒绝', e))\
                .then(lambda fn: os.remove(temp_fn))\

    def on_prv_show(self):
        Promise.resolve(None)\
            .then(lambda v: self._show_prv())\
            .catch(lambda e:  sysapp.sysapp.show_error_toast(f"查看失败 {e}"))

    def on_confirm(self):
        loading =  sysapp.sysapp.show_loading_toast('打印中')
        Promise.resolve(None)\
            .then(lambda v: self._confirm()) \
            .then(lambda v: ( sysapp.sysapp.logger.dispatch("on_print", self.file_view.file), print('打印'))) \
            .then(lambda v:  sysapp.sysapp.show_success_toast("打印成功"))\
            .catch(lambda e:  sysapp.sysapp.show_error_toast(f"打印失败 {e}"))\
            .then(lambda v: loading.dismiss())

    def on_cancel(self):
        self.dismiss()

    def _select_path(self):
        fn = asksaveasfilename(
            title='存储为PNG图片',
            defaultextension=".png"
        )
        if fn:
            self.output_path = fn

    def _generate_param(self):
        fsize   = int(float(self.fsize))
        if fsize < 10 or fsize > 500:
            raise Exception("字体大小不规范")
        ang     = float(self.ang)
        lgap    = int(float(self.lgap))
        cgap    = int(float(self.cgap))
        opc     = int(float(self.opc))
        if opc < 0 or opc > 255:
            raise Exception("不透明度大小不规范")
        return fsize, ang, lgap, cgap, opc

    def _generate_prv(self, param):
        """
        参数
        :param param: (fsize, ang, lgap, cgap, opc)
        :return:
        """
        fn, fsize, ang, lgap, cgap, opc = param
        if self.water:
            fnt         = ImageFont.truetype(open('resource/fonts/pingfang.ttf', 'rb'), fsize, encoding='utf-8')  # 设置默认水印字体
            ImageFont.ImageFont.font = ImageDraw.ImageDraw.font = fnt
            ctt         = self.file_view.file.watermask_name    # 水印文字内容
            im          = Image.open(fn).convert('RGBA')
            wtmk_im     = Image.new("RGBA", (max(ImageFont.ImageFont().getsize(ctt)), ) * 2, (255, 255, 255, 0))
            dr_wtmk_im  = ImageDraw.Draw(wtmk_im)
            dr_wtmk_im.text((0, (wtmk_im.size[1] - fsize) / 2), ctt, fill=(0, 0, 0, opc)) # 一个水印图片
            wtmk_im     = wtmk_im.rotate(ang)
            wtmks_im    = Image.new("RGBA", im.size, (255, 255, 255, 0))
            for line in range(0, im.height, wtmk_im.height + lgap):
                for col in range(0, im.width, wtmk_im.width + cgap):
                    wtmks_im.paste(wtmk_im, (col, line))
            im = Image.alpha_composite(im, wtmks_im)
        else:
            im = Image.open(fn)
        self.prv_img = im
        im = im.resize((int(self.disp_width), int(im.height * self.disp_width / im.width)))
        return fn

    def _disp_prv(self, fn):
        self.prv_img.save(fn)
        self.prv_img_widget.source = fn #
        return fn

    def _show_prv(self):
        self.prv_img.show()

    def _confirm(self):
        if self.output_path:
            self.prv_img_widget.export_to_png(self.output_path, scale=20)
        else:
            raise Exception("请选择导出路径")


class PrvImage(Img):
    pass

__all__ = ("PrintSetting", "PrvImage")