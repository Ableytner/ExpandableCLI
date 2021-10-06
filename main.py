from time import sleep
from threading import Thread

from core.startup_handler import StartupHandler
from helpers.plugin_helper import PluginHelper
from helpers.window_helper import WindowHelper
from helpers.cli_helper import CLIHelper

class Main():
    def __init__(self, log_dir = "D:\AverageActiveTime\\", cache_dir = "D:\AverageActiveTime\\") -> None:
        self.window_helper = WindowHelper()
        self.plugin_helper = PluginHelper()
        self.start_handler = StartupHandler(cache_dir)
        self.cli_helper = CLIHelper(self)

        self.logging = True

        self.cache_dir = cache_dir
        self.log_dir = log_dir

        self.cli_thread = None

    def main(self):
        if not self.start_handler.main():
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
