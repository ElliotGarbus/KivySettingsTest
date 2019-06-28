from kivy.uix.settings import SettingPath, SettingItem
from kivy.uix.popup import Popup
from kivy.properties import StringProperty, ObjectProperty
from kivy.lang import Builder
import os

KV = """
#: import drivepath drivepath
<DirectoryDialog>:
    size_hint_x: None
    width: '500dp'
    BoxLayout:
        orientation: 'vertical'
        FileChooserListView:
            id: fc
            path: root.path
            dirselect: True
            filters: ['!*.']
        SettingSpacer:
        BoxLayout:
            size_hint_y: None
            height: '50dp'
            spacing: '5dp'
            padding: [0, 0, 0, dp(2.5)] # [padding_left, padding_top, padding_right, padding_bottom]
            Spinner:
                text:'Drive'
                values: drivepath.get_drive_names()
                on_text: fc.path = drivepath.get_path(self.text)
            Label:
                text_size: self.size
                halign: 'center'
                valign: 'center'
                shorten: True
                text: 'Dir: ' + ('<None>' if not fc.selection else fc.selection[0])
        BoxLayout:
            size_hint_y: None
            height: '50dp'
            spacing: '5dp'
            padding: [0, dp(2.5), 0, 0 ] # [padding_left, padding_top, padding_right, padding_bottom]
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
Builder.load_string(KV)

setting_panel_kv = """
<SettingDrivePathShort>:
    Label:
        text: root.value or ''
        pos: root.pos
        font_size: '15sp'
        text_size: self.size
        halign: 'center'
        valign: 'center'
        shorten: True
"""
Builder.load_string(setting_panel_kv)


class DirectoryDialog(Popup):
    path = StringProperty()    # The path of the dir to view
    action = ObjectProperty()  # action to execute on ok

    def __init__(self, **kwargs):
        self.path = kwargs['path']
        self.action = kwargs['action']
        super().__init__(**kwargs)


class SettingDrivePath(SettingPath):
    """Implementation of DrivePath setting on top of a :class:`SettingPath`.
    It extends SettingPath with a new popup, DirectoryDialog that allows the selection of a drive.
    The filter selected in the popup will only show directories.
    """
    def set_new_path(self, new_path):
        self.value = new_path

    def _create_popup(self, instance):
        initial_path = self.value or os.getcwd()
        popup = DirectoryDialog(title=self.title, path=initial_path, action=self.set_new_path)
        popup.open()


class SettingDrivePathShort(SettingItem):
    """Implementation of DrivePath setting on top of a :class:`SettingItem`.
    It extends SettingPath with a new popup, DirectoryDialog that allows the selection of a drive.
    The filter selected in the popup will only show directories.
    This class uses a KV string to change the display of the text on the settings panel.
    This behavior is defined by the KV class <SettingDrivePathShort>, in the KV string defined earlier is this file.
    """
    def on_panel(self, instance, value):
        if value is None:
            return
        self.fbind('on_release', self._create_popup)

    def set_new_path(self, new_path):
        self.value = new_path

    def _create_popup(self, instance):
        initial_path = self.value or os.getcwd()
        popup = DirectoryDialog(title=self.title, path=initial_path, action=self.set_new_path)
        popup.open()

