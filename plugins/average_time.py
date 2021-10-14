from datetime import datetime
from time import sleep

import helpers.config_helper as config_helper
from plugins.info_module_base import InfoModuleBase
from plugins.better_thread import BetterThread

class AverageTime(InfoModuleBase):
    def __init__(self) -> None:
        self.update_thread = None

    def get_pluginname(self):
        return "average_time"

    def depends_on(self):
        return ["better_thread"]

    def needs_startup(self):
        return True

    def get_info(self):
        helptext = ""

        helptext += "Showing help for the average_time plugin:\n"
        helptext += "average --> Calculates the average active time\n"
        helptext += "today --> Calculates the total time today"

        return helptext

    def start(self):
        self.update_thread = BetterThread(target=self.update_controller)

        timeNow = datetime.now()

        with open(config_helper.get_setting("path") + "timefile.txt", "a+") as logfile:
            log_text = ""
            #log_text.append("[" + str(timeNow).split(" ")[0] + "|STARTUP] " + str(timeNow).split(" ")[1] + "\n")
            #log_text.append("[" + str(timeNow).split(" ")[0] + "|SHUTOFF] " + str(timeNow).split(" ")[1] + "\n")
            log_text += "[" + str(timeNow).replace(" ", "|").split(".")[0]
            log_text += "|STARTUP]\n"

            log_text += "[" + str(timeNow).replace(" ", "|").split(".")[0]
            log_text += "|SHUTOFF]\n"

            logfile.writelines(log_text)

        self.update_thread.start()


    def execute(self, command):
        if command == "average":
            return self._calculate_average()
        elif command == "today":
            return self._calculate_today()
        else:
            print("Unknown command " + command + "!")

    def exit(self):
        print("Waiting for update_thread to exit...")
        self.update_thread.exit()
        print("update_thread gracefully stopped")

    def _calculate_average(self):
        print("calculate_average isn't yet implemented!")

    def _calculate_today(self):
        print("calculate_today isn't yet implemented!")

    def update_controller(self):
        while True:
            if self.update_thread.stopped():
                return
            self.update_function()
            sleep(5)

    def update_function(self):
        timeNow = datetime.now()

        with open(config_helper.get_setting("path") + "timefile.txt", "r") as logfile:
            lines = logfile.readlines()

        with open(config_helper.get_setting("path") + "timefile.txt", "w") as logfile:
            lines[-1] = "[" + str(timeNow).replace(" ", "|").split(".")[0] + "|SHUTOFF]\n"

            logfile.writelines(lines)
