# @author Emanuel Ableitners
# github: https://github.com/EmanuelAbleitner

from sys import argv
from time import sleep

from core.logging import log, LoggingType

import helpers.config_helper as config_helper
from helpers.plugin_helper import PluginHelper
from helpers.window_helper import WindowHelper
from helpers.cli_helper import CLIHelper

class Main():
    def __init__(self) -> None:
        try:
            log(__file__, LoggingType.info, "Successfully read setting logging as " + str(config_helper.get_setting("logging")))
        except:
            config_helper.save_setting("logging", False)
            log(__file__, LoggingType.warning, "Saved new setting logging as " + str(config_helper.get_setting("logging")))

        self.window_helper = WindowHelper()
        self.plugin_helper = PluginHelper()
        self.cli_helper = CLIHelper(self.plugin_helper)
        log(__file__, LoggingType.info, "Successfully initialized helpers")

        self.cli_thread = None

    def main(self):
        if not self.window_helper.background_program_running():
            print("Running instance detected, exiting...")
            log(__file__, LoggingType.info, "Running instance detected, exiting...")
            sleep(1.5)
            exit()

        self.plugin_helper.init_plugins()
        self.plugin_helper.check_comp()
        if "--hide" in argv:
            self.window_helper.hide_cli()
        else:
            self.plugin_helper.start_plugins()
        log(__file__, LoggingType.info, "Plugin loading finished successfully")

        log(__file__, LoggingType.info, "Starting cli_helper...")
        self.cli_helper.start()
        log(__file__, LoggingType.info, "Success")

        log(__file__, LoggingType.info, "Startup finished successfully")

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
