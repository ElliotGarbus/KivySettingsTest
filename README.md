# Creating a new SettingItem in Kivy 

A setting item is used to set a specific configuration value in a settings panel.  The current documentation does not include
how to create a new SettingsItem.  This code creates 2 new setting items:

* **drivepath:** A dialog similar to path, but features a drive selection spinner.  It is derived from path.
* **drivepath_short:** Similar to drivepath, but shortens long file paths in the settings panel. It is derived from SettingItem.

## Overview
Creating a new setting item requires changes to code in a number of places:

1. The creation of the new settingitem, derived from an existing setting item, or a SettingItem.  If the the SettingItems is derived
directly from SettingItem, KV code must be provided to format the data on the panel.
1. Registering the new setting type and associating it with newly created SettingItem. This is done in the App method build_settings()
1. Creating a JSON file or JSON String to define the settings panel.
1. Calling add_json_panel() from build_settings(), using the JSON data above to create the panel.
1. Setting the config defaults in the App method build_config()

## Files:
**main.py** This is a modified version of the settings example found in kivy-examples/settings.   Found is this file:
* The JSON string used to create the settings panel
* The calls in build_config() to config.setdefaults() that set the default values if the .ini file has not been created.
* The call in build_settings() to settings.register_type() that associate the new type name, found in the JSON file, with the specific SettingItem class for that type.
* The call in build_settings() to settings.add_json_panel() to create the panel from the JSON string.


**drivepathsetting.py** This file defined the new setting items.
* Note the KV code under '<SettingDrivePathShort>' is used to format the string in the settings panel.
* This file demonstrates using KV code to create the dialogs for the setting items. 

**drivepath.py** This is a utility for reading the disk drive names on a Windows System, there are also behaviors defined for MacOS and Linux.


  
