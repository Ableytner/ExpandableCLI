# @author Emanuel Ableitners
# github: https://github.com/EmanuelAbleitner

from time import sleep
from threading import Thread

import helpers.config_helper as config_helper
from core.logging import log, LoggingType
from helpers.plugin_helper import PluginHelper
from helpers.window_helper import WindowHelper
from helpers.cli_helper import CLIHelper

class Main():
    def __init__(self, path = "D:\AverageActiveTime\\") -> None:
        self.window_helper = WindowHelper(path)
        self.plugin_helper = PluginHelper()
        self.cli_helper = CLIHelper(self.plugin_helper)

        self.cli_thread = None

        config_helper.save_setting("path", path)

        try:
            config_helper.get_setting("logging")
        except:
            config_helper.save_setting("logging", False)

        log(__file__, LoggingType.info, "Test")

    def main(self):
        if not self.window_helper.background_program_running():
            print("Running instance detected, exiting...")
            sleep(3)
            exit()

        self.plugin_helper.init_plugins()
        self.plugin_helper.check_comp()
        self.plugin_helper.start_plugins()

        self.cli_helper.start()

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

if __name__ == "__main__":
    Main().main()
