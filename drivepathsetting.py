from kivy.uix.settings import SettingItem, SettingPath
from kivy.uix.popup import Popup
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
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
                disabled: len(fc.selection) == 0
                on_release: 
                    root.action(fc.selection[0])
                    root.dismiss()
            Button:
                text: 'Cancel'
                on_release: root.dismiss() 
"""

setting_panel_kv = """
<SettingDrivePath>:
    Label:
        text: root.value or ''
        pos: root.pos
        font_size: '15sp'
"""
# Builder.load_string(setting_panel_kv)
Builder.load_string(KV)


class DirectoryDialog(Popup):
    path = StringProperty()    # The path of the dir to view
    action = ObjectProperty()  # action to execute on ok

    def __init__(self, **kwargs):
        self.path = kwargs['path']
        self.action = kwargs['action']
        super().__init__(**kwargs)


class SettingDrivePath(SettingPath):
    def set_new_path(self, new_path):
        self.value = new_path

    def _create_popup(self, instance):
        initial_path = self.value or os.getcwd()
        popup = DirectoryDialog(title=self.title, path=initial_path, action=self.set_new_path)
        popup.open()
