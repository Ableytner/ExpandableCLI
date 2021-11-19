from datetime import datetime
from time import sleep

import helpers.config_helper as config_helper
from plugins.base_plugin import BasePlugin
from core.better_thread import BetterThread

class AverageTime(BasePlugin):
    def __init__(self) -> None:
        super().__init__()
        self.update_thread = None
        self._thread_stopped = True

    def get_pluginname(self):
        return "average_time"

    def needs_startup(self):
        return True

    def get_info(self):
        helptext = ""

        helptext += "Showing help for the average_time plugin:\n"
        helptext += "average --> Calculates the average active time\n"
        helptext += "today --> Calculates the total time today"

        return helptext

    def start(self):
        super().start()

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
        self._thread_stopped = False

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
        while not self._thread_stopped:
            sleep(0.5)
        print("update_thread gracefully stopped")

    def _calculate_average(self):
        print("calculate_average isn't yet implemented!")

    def _calculate_today(self):
        print("calculate_today isn't yet implemented!")

    def update_controller(self):
        while True:
            if self.update_thread.stopped():
                self._thread_stopped = True
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

    def format_to_seconds(self, time):
        return float(time[0]) * 3600 + float(time[1]) * 60 + float(time[2])

    def format_to_time(self, seconds):
        minutes = 0
        hours = 0

        while seconds >= 60:
            seconds -= 60
            minutes += 1

        while minutes >= 60:
            minutes -= 60
            hours += 1

        return [hours, minutes, seconds]
