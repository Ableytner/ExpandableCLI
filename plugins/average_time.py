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
        helptext += "today --> Calculates the total time today\n"
        helptext += "session --> Calculates the current session time"

        return helptext

    def start(self):
        super().start()

        self.update_thread = BetterThread(target=self.update_controller)

        timeNow = datetime.now().timestamp()

        with open(config_helper.get_setting("path") + "timefile.txt", "a+") as logfile:
            log_text = ""
            # log_text += "[" + str(timeNow).replace(" ", "|").split(".")[0]
            log_text += "[" + str(int(timeNow))
            log_text += "|STARTUP]\n"

            # log_text += "[" + str(timeNow).replace(" ", "|").split(".")[0]
            log_text += "[" + str(int(timeNow))
            log_text += "|SHUTOFF]\n"

            logfile.writelines(log_text)

        self.update_thread.start()
        self._thread_stopped = False

    def execute(self, command):
        if command == "average":
            return self._calculate_average()
        elif command == "today":
            return self._calculate_today()
        elif command == "session":
            return self._calculate_session()
        else:
            print("Unknown command " + command + "!")

    def exit(self):
        print("Waiting for update_thread to exit...")
        self.update_thread.exit()
        while not self._thread_stopped:
            sleep(0.5)
        print("update_thread gracefully stopped")

    def _calculate_average(self):
        timeint = int(datetime.now().timestamp())
        print(timeint)
        print(datetime.fromtimestamp(timeint))

        print("calculate_average isn't yet implemented!")

    def _calculate_today(self):
        with open(config_helper.get_setting("path") + "timefile.txt", "r") as logfile:
            lines = logfile.readlines()
        starttimeint = int(lines[-2][1:-1:].split("|")[0])
        stoptimeint = int(lines[-1][1:-1:].split("|")[0])

        start_datetime = datetime.fromtimestamp(starttimeint)
        stop_datetime = datetime.fromtimestamp(stoptimeint)
        if start_datetime.date() != stop_datetime.date():
            print("Today this computer has been running for " + str(stop_datetime.time()) + "!")
        else:
            print("Today this computer has been running for " + str(stop_datetime - start_datetime) + "!")

    def _calculate_session(self):
        with open(config_helper.get_setting("path") + "timefile.txt", "r") as logfile:
            lines = logfile.readlines()
        starttimeint = int(lines[-2][1:-1:].split("|")[0])
        stoptimeint = int(lines[-1][1:-1:].split("|")[0])
        sessiontime = datetime.fromtimestamp(stoptimeint) - datetime.fromtimestamp(starttimeint)
        print("This computer has been running for " + str(sessiontime) + "!")

    def update_controller(self):
        while True:
            if self.update_thread.stopped():
                self._thread_stopped = True
                return
            self.update_function()
            sleep(5)

    def update_function(self):
        timeNow = datetime.now().timestamp()

        with open(config_helper.get_setting("path") + "timefile.txt", "r") as logfile:
            lines = logfile.readlines()

        with open(config_helper.get_setting("path") + "timefile.txt", "w") as logfile:
            lines[-1] = "[" + str(int(timeNow)) + "|SHUTOFF]\n"
            # lines[-1] = "[" + str(timeNow).replace(" ", "|").split(".")[0] + "|SHUTOFF]\n"

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
