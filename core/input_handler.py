from time import sleep

from helpers.window_helper import WindowHelper

class InputHandler():
    def __init__(self, main) -> None:
        self.main = main
        self.plugin_helper = main.plugin_helper

    def handle_input(self, input_value):
        if input_value == "help":
            print(self._get_helptext(self.main))
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
            self.main.logging = not self.main.logging
            print("Toggled logging to " + str(self.main.logging) + "!")
        elif input_value == "plugins":
            print("Printing " + str(len(self.plugin_helper.plugin_list)) + " installed plugins:")
            for plugin in self.plugin_helper.plugin_list:
                print(plugin.inst.get_pluginname())
        elif len(input_value.split(" ")) > 1:
            self.plugin_helper.execute(input_value)
        else:
            for plugin in self.plugin_helper.plugin_list:
                if input_value == plugin.inst.get_pluginname():
                    print(plugin.inst.get_info())
                    return
            print("Unknown command " + input_value + "!")

    @staticmethod
    def _get_helptext(main):
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
        helptext += "logs --> Enables/disables logging (current: " + str(main.logging) + ")\n"
        helptext += " --------------- debug commands  --------------- \n"
        helptext += "plugins --> Shows all loaded plugins\n"
        helptext += " --------------- plugin commands --------------- \n"
        helptext += "[plugin_name] help --> Shows a helptext for the given plugin\n"
        helptext += "[plugin_name] [command] --> Executes the command from the given plugin\n"
        helptext += " =============== end of the helptext     =============== "

        return helptext
