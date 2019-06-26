from kivy.uix.settings import SettingItem, SettingSpacer
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.metrics import dp


from kivy.lang import Builder


import os

KV = """
#: import drivepath drivepath
<DirectoryDialog>:
    size_hint: None,.9
    width: dp(500)
    auto_dismiss: False
    BoxLayout:
        orientation: 'vertical'
        FileChooserListView:
            id: fc
            path: root.path
            dirselect: True
            filters: ['!*.']
        BoxLayout:
            size_hint_y: .1
            Spinner:
                size_hint_x: 0.5
                text:'Drive'
                values: drivepath.get_drive_names()
                on_text: fc.path = drivepath.get_path(self.text)
            Label:
                size_hint_x: 0.5
                text_size: self.size
                halign: 'center'
                valign: 'center'
                shorten: True
                text: 'Dir: ' + ('<None>' if not fc.selection else fc.selection[0])
        BoxLayout:
            size_hint_y: .1
            orientation: 'horizontal'
            Button:
                text: 'Ok'
                disabled: 0==len( fc.selection )
                on_release:
                    root.action(fc.selection[0])
                    root.dismiss()
            Button:
                text: 'Cancel'
                on_release: 
                    root.dismiss()
                    
                    
"""


class DirectoryDialog(Popup):
    path = StringProperty()    # The path of the dir to view
    action = ObjectProperty()  # action to execute on ok
    instance = ObjectProperty()

    def __init__(self, **kwargs):
        self.path = kwargs['path']
        self.action = kwargs['action']
        self.instance = kwargs['instance']
        super().__init__(**kwargs)


class SettingDrivePath(SettingItem):
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)

    original = True   # If original is True, then use code from settingspath, else use my code.
    if original:
        popup = ObjectProperty(None, allownone=True)
        textinput = ObjectProperty(None)
        show_hidden = BooleanProperty(False)
        dirselect = BooleanProperty(True)

        def on_panel(self, instance, value):
            if value is None:
                return
            self.fbind('on_release', self._create_popup)

        def _dismiss(self, *largs):
            if self.textinput:
                self.textinput.focus = False
            if self.popup:
                self.popup.dismiss()
            self.popup = None

        def _validate(self, instance):
            self._dismiss()
            value = self.textinput.selection

            if not value:
                return

            self.value = os.path.realpath(value[0])
            print(f'path: {self.value}, textinput: {self.textinput.selection}')

        def _create_popup(self, instance):
            # create popup layout
            content = BoxLayout(orientation='vertical', spacing=5)
            popup_width = dp(500)
            self.popup = popup = Popup(
                title=self.title, content=content, size_hint=(None, 0.9),
                width=popup_width)

            # create the filechooser
            initial_path = self.value or os.getcwd()
            self.textinput = textinput = FileChooserListView(
                path=initial_path, size_hint=(1, 1),
                dirselect=self.dirselect, show_hidden=self.show_hidden)
            textinput.bind(on_path=self._validate)

            # construct the content
            content.add_widget(textinput)
            content.add_widget(SettingSpacer())

            # 2 buttons are created for accept or cancel the current value
            btnlayout = BoxLayout(size_hint_y=None, height='50dp', spacing='5dp')
            btn = Button(text='Ok')
            btn.bind(on_release=self._validate)
            btnlayout.add_widget(btn)
            btn = Button(text='Cancel')
            btn.bind(on_release=self._dismiss)
            btnlayout.add_widget(btn)
            content.add_widget(btnlayout)

            # all done, open the popup !
            popup.open()
    else:    #  My code
        def on_panel(self, instance, value):
            if value is None:
                return
            self.fbind('on_release', self._create_popup)

        def set_new_path(self, new_path):
            self.value = new_path

        def _create_popup(self, instance):
            content = Builder.load_string(KV)
            initial_path = self.value or os.getcwd()
            popup = DirectoryDialog(title=self.title,
                                    path=initial_path,
                                    action=self.set_new_path,
                                    instance=instance)
            popup.open()
