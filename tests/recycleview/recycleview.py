from kivy.app import App
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

Builder.load_string('''
<SelectableLabel>:
    # Draw a background to indicate selection
    canvas.before:
        Color:
            rgba: (1, 0, 1, .5) if self.selected else (0, 0, 0, 1)
        Rectangle:
            pos: self.pos
            size: self.size
<RV>:
    viewclass: 'SelectableLabel'
    SelectableRecycleBoxLayout:
        canvas:
            Color:
                rgba: (1, 1, 0,1)
            Rectangle:
                pos: self.pos
                size: self.size
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        multiselect: True
        touch_multiselect: True
''')


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return False
        if self.collide_point(*touch.pos) and self.selectable:
            try:
                for one_color in self.parent.children:
                    if one_color.selected:
                        one_color.selected = False
                    if self.parent.parent.data[self.index]["text"]==one_color.text:
                        self.parent.parent.data_selected[0]=one_color.text
                        one_color.selected=True
            except:
                pass
class RV(RecycleView):
    def __init__(self,data_range=range(2000,2100),**kwargs):
        super(RV, self).__init__(**kwargs)
        self.data_selected=[0]
        self.data = [{'text': str(x)} for x in data_range]

class TestApp(App):
    def build(self):
        return RV()

if __name__ == '__main__':
    TestApp().run()
