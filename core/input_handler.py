import os
from time import sleep

from core.logging import log, LoggingType
import helpers.config_helper as config_helper
from helpers.window_helper import WindowHelper
from helpers.plugin_helper import PluginHelper

class InputHandler():
    def __init__(self, plugin_helper: PluginHelper, cli_helper) -> None:
        self.plugin_helper = plugin_helper
        self.cli_helper = cli_helper

    def handle_input(self, input_value):
        log(__file__, "Processing command " + input_value)
        # a match-case construct for handling the input
        match input_value:
            case "help":
                print(self._get_helptext())
                return
            case "hide":
                print("Hiding...")
                sleep(3)
                WindowHelper().hide_cli()
                return
            case "clear":
                print("Clearing console window...")
                WindowHelper().clear()
                print("Console window cleared!")
                return
            case "logs":
                self._toggle_logs()
                return
            case "plugins":
                self.plugin_helper.print_plugins()
                return
            case "plugins reload":
                self._reload_plugins()
                return
            case "stop" | "exit" | "quit" | "q":
                self._exit()
                return

        # if none of the match-cases fitted
        if input_value.split(" ")[0] == "disable":
            pluginname = input_value.split(" ")[1]
            self.plugin_helper.disable_plugin(pluginname)
            log(__file__, "Disabled plugin " + pluginname, printout=True)
            log(__file__, "use 'plugins reload' for the changes to take effect", printout=True)
        elif input_value.split(" ")[0] == "enable":
            pluginname = input_value.split(" ")[1]
            self.plugin_helper.enable_plugin(pluginname)
            log(__file__, "Enabled plugin " + pluginname, printout=True)
            log(__file__, "use 'plugins reload' for the changes to take effect", printout=True)
        elif len(input_value.split(" ")) > 1:
            self.plugin_helper.start_plugins()
            self.plugin_helper.execute(input_value)
        else:
            for plugin in self.plugin_helper.plugin_list:
                if input_value == plugin.inst.get_pluginname():
                    # print the helptext if the command is only a plugin name
                    self.plugin_helper.start_plugins()
                    print(plugin.inst.get_info())
                    return
            # if the command is unknown
            log(__file__, "Unknown command '" + input_value + "'!", LoggingType.warning, printout=True)

    def _exit(self):
        # exit function, called if the command is stop, exit, quit or q
        log(__file__, "Exiting plugins...", printout=True)
        self.plugin_helper.exit_plugins()
        log(__file__, "All plugins exited, closing program...", printout=True)
        self.cli_helper.exit = True
        self.cli_helper.cli_thread.exit()
        sleep(1.5)
        exit()

    def _toggle_logs(self):
        # toggles if logging is enabled or disabled
        try:
            logging_state = config_helper.get_setting("logging")
            if logging_state == True or logging_state == False:
                config_helper.save_setting("logging", not logging_state)
                print("Toggled logging to " + str(config_helper.get_setting("logging")) + "!")
        except Exception as e:
            log(__file__, "An error occured during reading the config: " + str(e), LoggingType.error, printout=True)

    def _reload_plugins(self):
        # exits all plugins and starts them again, needed after enabling/disabling plugins
        log(__file__, "Exiting plugins...", printout=True)
        self.plugin_helper.exit_plugins()
        log(__file__, "Plugins exited successfully, loading plugins...", printout=True)
        self.plugin_helper.init_plugins()
        self.plugin_helper.check_comp()
        self.plugin_helper.startup_plugins()
        log(__file__, "Plugin reloading finished successfully")

    @staticmethod
    def _get_helptext():
        # returns the general helptext as a string
        helptext = ""

        helptext += " =============== start of the helptext =============== \n"
        helptext += "Showing help for the core module:\n"
        helptext += " --------------- main commands   --------------- \n"
        helptext += "help --> Shows this helptext\n"
        helptext += "hide --> Hides the cli\n"
        helptext += "clear --> Clears the console window\n"
        helptext += "stop | exit | quit | q --> Exits the cli\n"
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
