from time import sleep
from helpers.window_helper import WindowHelper

class InputHandler():
    def __init__(self, main) -> None:
        self.plugin_helper = main.plugin_helper

        self.main = main

    def handle_input(self, input_value):
        if input_value == "help":
            print(self._get_helptext(self.main))
        elif input_value == "hide":
            print("Hiding...")
            sleep(3)
            WindowHelper().hide_cli()
        elif input_value == "clear":
            print("Clearing console window...")
            pass
            print("Console window cleared!")
        elif input_value == "exit" or input_value == "stop":
            print("Method to stop the program isn't yet implemented!")
            pass
        elif len(input_value.split(" ")) > 1:
            self.plugin_helper.execute(input_value)
        else:
            print("Unknown command " + input_value + "!")

    @staticmethod
    def _get_helptext(main):
        helptext = ""

        helptext += "Showing help for the average_active_time module:\n"
        helptext += "help --> Shows this helptext\n"
        helptext += "hide --> Hides the cli\n"
        helptext += "clear --> Clears the console window\n"
        helptext += "logs --> Enables/disables logging (current: " + str(main.logging) + ")"

        return helptext
