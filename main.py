"""
This is an example of creating a custom setting item in a settings panel.
This file is extended from the Config Example from the kivy-examples/settings
==============

This file contains a simple example of how the use the Kivy settings classes in
a real app. It allows the user to change the caption and font_size of the label
and stores these changes.

It has been extended to show how to integrate 2 custom panel items:
drivepath: A dialog similar to path, but features a drive selection spinner
drivepath_short: Similar to drivepath, but shortens long file paths in the settings panel

When the user next runs the programs, their changes are restored.

"""

from kivy.app import App
from kivy.uix.settings import SettingsWithTabbedPanel
from kivy.logger import Logger
from kivy.lang import Builder
import drivepathsetting


# We first define our GUI
kv = '''
BoxLayout:
    orientation: 'vertical'
    Button:
        text: 'Configure app (or press F1)'
        on_release: app.open_settings()
    Label:
        id: label
        text: 'Hello'
'''

# This JSON defines entries we want to appear in our App configuration screen
json = '''
[
    {
        "type": "string",
        "title": "Label caption",
        "desc": "Choose the text that appears in the label",
        "section": "My Label",
        "key": "text"
    },
    {
        "type": "numeric",
        "title": "Label font size",
        "desc": "Choose the font size the label",
        "section": "My Label",
        "key": "font_size"
    },
     {
        "type": "bool",
        "title": "A Choice",
        "desc": "A switch: On or Off",
        "section": "DEFAULT FILE PATH",
        "key": "B0"
    },
    {
        "type": "path",
        "title": "The default path input",
        "desc": "Select a path",
        "section": "DEFAULT FILE PATH",
        "key": "path_1"
    },
    {
        "type": "drivepath",
        "title": "Drive Path test",
        "desc": "Extends path setting by supporting a drive",
        "section": "DEFAULT FILE PATH",
        "key": "path_2"
    },
    {
        "type": "drivepath_short",
        "title": "Drive Path Short test",
        "desc": "Test the drive path chooser, displays a short path",
        "section": "DEFAULT FILE PATH",
        "key": "path_3"
    }
]
'''


class MyApp(App):
    def build(self):
        """
        Build and return the root widget.
        """
        # The line below is optional. You could leave it out or use one of the
        # standard options, such as SettingsWithSidebar, SettingsWithSpinner
        # etc.
        self.settings_cls = MySettingsWithTabbedPanel

        # We apply the saved configuration settings or the defaults
        root = Builder.load_string(kv)
        label = root.ids.label
        label.text = self.config.get('My Label', 'text')
        label.font_size = float(self.config.get('My Label', 'font_size'))
        return root

    def build_config(self, config):
        """
        Set the default values for the configs sections.
        """
        config.setdefaults('My Label', {'text': 'Hello', 'font_size': 20})
        config.setdefaults('DEFAULT FILE PATH', {'B0': '0',
                                                 'path_1': '.',
                                                 'path_2': '.',
                                                 'path_3': '.'})

    def build_settings(self, settings):
        """
        Add our custom section to the default configuration object.
        """
        # We use the string defined above for our JSON, but it could also be
        # loaded from a file as follows:
        #     settings.add_json_panel('My Label', self.config, 'settings.json')
        settings.register_type('drivepath', drivepathsetting.SettingDrivePath)
        settings.register_type('drivepath_short', drivepathsetting.SettingDrivePathShort)
        settings.add_json_panel('My Label', self.config, data=json)

    def on_config_change(self, config, section, key, value):
        """
        Respond to changes in the configuration.
        """
        Logger.info("main.py: App.on_config_change: {0}, {1}, {2}, {3}".format(
            config, section, key, value))

        if section == "My Label":
            if key == "text":
                self.root.ids.label.text = value
            elif key == 'font_size':
                self.root.ids.label.font_size = float(value)

    def close_settings(self, settings=None):
        """
        The settings panel has been closed.
        """
        Logger.info("main.py: App.close_settings: {0}".format(settings))
        super(MyApp, self).close_settings(settings)


class MySettingsWithTabbedPanel(SettingsWithTabbedPanel):
    """
    It is not usually necessary to create subclass of a settings panel. There
    are many built-in types that you can use out of the box
    (SettingsWithSidebar, SettingsWithSpinner etc.).

    You would only want to create a Settings subclass like this if you want to
    change the behavior or appearance of an existing Settings class.
    """
    def on_close(self):
        Logger.info("main.py: MySettingsWithTabbedPanel.on_close")

    def on_config_change(self, config, section, key, value):
        Logger.info(
            "main.py: MySettingsWithTabbedPanel.on_config_change: "
            "{0}, {1}, {2}, {3}".format(config, section, key, value))


MyApp().run()
