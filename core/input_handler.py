import os
from time import sleep

import helpers.config_helper as config_helper
from helpers.window_helper import WindowHelper

class InputHandler():
    def __init__(self, plugin_helper) -> None:
        self.plugin_helper = plugin_helper

    def handle_input(self, input_value):
        if input_value == "help":
            print(self._get_helptext())
        elif input_value == "hide":
            print("Hiding...")
            sleep(3)
            WindowHelper().hide_cli()
        elif input_value == "clear":
            print("Clearing console window...")
            WindowHelper().clear()
            print("Console window cleared!")
        elif input_value == "stop" or input_value == "exit":
            print("Exiting program...")
            self.plugin_helper.exit_plugins()
            exit()
        elif input_value == "logs":
            try:
                logging_state = config_helper.get_setting("logging")
                if logging_state == True or logging_state == False:
                    config_helper.save_setting("logging", not logging_state)
            except Exception as e:
                print("An error occured during reading the config: ", e)
            finally:
                print("Toggled logging to " + str(config_helper.get_setting("logging")) + "!")
        elif input_value == "plugins":
            print("Printing " + str(len(self.plugin_helper.plugin_list)) + " installed plugins:")
            for plugin in self.plugin_helper.plugin_list:
                print(plugin.inst.get_pluginname())
        elif input_value == "test":
            print("Test detected...")
            config_helper.save_setting("testkey", "testvalue")
            config_helper.save_setting("testkey", "testvaluee")
            config_helper.save_setting("testkey2", "testvalue2")
            config_helper.save_setting("testkey3", "testvalue3")
            config_helper.save_setting("testkey4", "testvalue4")
            print(config_helper.get_settings())
            print(config_helper.get_setting("testkey2"))
        elif len(input_value.split(" ")) > 1:
            self.plugin_helper.execute(input_value)
        else:
            for plugin in self.plugin_helper.plugin_list:
                if input_value == plugin.inst.get_pluginname():
                    print(plugin.inst.get_info())
                    return
            print("Unknown command " + input_value + "!")

    @staticmethod
    def _get_helptext():
        helptext = ""

        helptext += " =============== start of the helptext =============== \n"
        helptext += "Showing help for the core module:\n"
        helptext += " --------------- main commands   --------------- \n"
        helptext += "help --> Shows this helptext\n"
        helptext += "hide --> Hides the cli\n"
        helptext += "clear --> Clears the console window\n"
        helptext += "stop --> Exits the cli\n"
        helptext += "exit --> Exits the cli\n"
        helptext += " --------------- main options    --------------- \n"
        helptext += "logs --> Enables/disables logging (current: " + str(config_helper.get_setting("logging")) + ")\n"
        helptext += " --------------- debug commands  --------------- \n"
        helptext += "plugins --> Shows all loaded plugins\n"
        helptext += " --------------- plugin commands --------------- \n"
        helptext += "[plugin_name] help --> Shows a helptext for the given plugin\n"
        helptext += "[plugin_name] [command] --> Executes the command from the given plugin\n"
        helptext += " =============== end of the helptext     =============== "

        return helptext
