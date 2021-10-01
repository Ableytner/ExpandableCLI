from datetime import datetime
from threading import Thread
from plugins.info_module_base import InfoModuleBase

class AverageTime(InfoModuleBase):
    def __init__(self) -> None:
        self.update_thread = None

    def get_modulename(self):
        return "average_time"

    def depends_on(self):
        return ["better_thread"]

    def get_info(self):
        helptext = ""

        helptext += "Showing help for the average_time module:\n"
        helptext += "average --> Calculates the average active time\n"
        helptext += "today --> Calculates the total time today"

        print(helptext)
        return helptext

    def get_info_raw(self):
        helptext = ""

        helptext += "average\n"
        helptext += "today"

        print(helptext)
        return helptext

    def start(self):
        self._start()

    def execute(self, command):
        if command == "average":
            return self._calculate_average()
        elif command == "today":
            return self._calculate_today()
        else:
            print("Unknown command " + command + "!")

    def _calculate_average(self):
        print("calculate_average isn't yet implemented!")

    def _calculate_today(self):
        print("calculate_today isn't yet implemented!")

    def _start(self):
        self.update_thread = Thread(target=self.update_function)

        timeNow = datetime.now()

        with open("D:\AverageActiveTime\logfile.txt", "a+") as logfile:
            log_text = []
            log_text.append("[" + str(timeNow).split(" ")[0] + "|STARTUP] " + str(timeNow).split(" ")[1] + "\n")
            log_text.append("[" + str(timeNow).split(" ")[0] + "|SHUTOFF] " + str(timeNow).split(" ")[1] + "\n")
            logfile.writelines(log_text)

        self.update_thread.start()

    def update(self):
        timeNow = datetime.now()

        with open("D:\AverageActiveTime\logfile.txt", "r") as logfile:
            lines = logfile.readlines()

        with open("D:\AverageActiveTime\logfile.txt", "w") as logfile:
            lines[-1] = "[" + str(timeNow).split(" ")[0] + "|SHUTOFF] " + str(timeNow).split(" ")[1] + "\n"

            logfile.writelines(lines)
