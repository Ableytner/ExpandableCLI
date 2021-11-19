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
        # read setting for logging
        # this needs to be executed at the very start because else it will crash at log(...)
        try:
            log(__file__, "Successfully read setting logging as " + str(config_helper.get_setting("logging")))
        except:
            # if the config doesn't contain the logging setting, save it as False
            config_helper.save_setting("logging", False)
            log(__file__, "Saved new setting logging as " + str(config_helper.get_setting("logging")), LoggingType.warning)

        # instantiate the helpers
        self.window_helper = WindowHelper()
        self.plugin_helper = PluginHelper()
        self.cli_helper = CLIHelper(self.plugin_helper)
        log(__file__, "Successfully initialized helpers")

        self.cli_thread = None

    def main(self):
        if self.window_helper.background_program_running():
            # if a running instance has been detected, this instance will exit
            log(__file__, "Running instance detected, exiting...", printout=True)
            sleep(1.5)
            exit()

        # manage plugins
        self.plugin_helper.init_plugins()
        self.plugin_helper.check_comp()
        self.plugin_helper.startup_plugins()
        log(__file__, "Plugin loading finished successfully")

        # hide program if flag --hide is set
        if "--hide" in argv:
            self.window_helper.hide_cli()

        # starts the cli thread listening for console inputs
        log(__file__, "Starting cli_helper...")
        self.cli_helper.start()
        log(__file__, "Success")

        log(__file__, "Startup finished successfully")

if __name__ == "__main__":
    Main().main()
