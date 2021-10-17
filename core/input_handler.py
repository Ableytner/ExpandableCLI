import os
from time import sleep

from core.logging import log, LoggingType
import helpers.config_helper as config_helper
from helpers.window_helper import WindowHelper
from helpers.plugin_helper import PluginHelper

class InputHandler():
    def __init__(self, plugin_helper: PluginHelper) -> None:
        self.plugin_helper = plugin_helper

    def handle_input(self, input_value):
        log(__file__, LoggingType.info, "Processing command " + input_value)
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
        elif input_value.split(" ")[0] == "disable":
            pluginname = input_value.split(" ")[1]
            log(__file__, LoggingType.info, "Disabling plugin " + pluginname)
            self.plugin_helper.disable_plugin(pluginname)
            log(__file__, LoggingType.info, "Disabling plugin " + pluginname)
        elif input_value.split(" ")[0] == "enable":
            pluginname = input_value.split(" ")[1]
            log(__file__, LoggingType.info, "Enabling plugin " + pluginname)
            self.plugin_helper.enable_plugin(pluginname)
            log(__file__, LoggingType.info, "Enabling plugin " + pluginname)
        elif input_value == "logs":
            try:
                logging_state = config_helper.get_setting("logging")
                if logging_state == True or logging_state == False:
                    config_helper.save_setting("logging", not logging_state)
                    #log(__file__, LoggingType.info, "Toggled logging to " + str(config_helper.get_setting("logging")) + "!", True)
                    print("Toggled logging to " + str(config_helper.get_setting("logging")) + "!")
            except Exception as e:
                log(__file__, LoggingType.error, "An error occured during reading the config: " + str(e))
                print("An error occured during reading the config: " + str(e))
        elif input_value == "plugins":
            log(__file__, LoggingType.info, "Printing " + str(len(self.plugin_helper.plugin_list)) + " installed plugins:", True)
            for plugin in self.plugin_helper.plugin_list:
                log(__file__, LoggingType.info, plugin.inst.get_pluginname(), True)
        elif len(input_value.split(" ")) > 1:
            self.plugin_helper.execute(input_value)
        else:
            for plugin in self.plugin_helper.plugin_list:
                if input_value == plugin.inst.get_pluginname():
                    print(plugin.inst.get_info())
                    return
            log(__file__, LoggingType.info, "Unknown command " + input_value + "!", True)

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
        helptext += "disable [plugin_name] --> Disable the given plugin\n"
        helptext += "enable [plugin_name] --> Enable the given plugin\n"
        helptext += " --------------- main options    --------------- \n"
        helptext += "logs --> Enables/disables logging (current: " + str(config_helper.get_setting("logging")) + ")\n"
        helptext += " --------------- debug commands  --------------- \n"
        helptext += "plugins --> Shows all loaded plugins\n"
        helptext += " --------------- plugin commands --------------- \n"
        helptext += "[plugin_name] help --> Shows a helptext for the given plugin\n"
        helptext += "[plugin_name] [command] --> Executes the command from the given plugin\n"
        helptext += " =============== end of the helptext     =============== "

        return helptext
