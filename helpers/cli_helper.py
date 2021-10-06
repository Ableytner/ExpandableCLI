from time import sleep
from threading import Thread

from core.input_handler import InputHandler
from plugins.better_thread import BetterThread

class CLIHelper():
    def __init__(self, main) -> None:
        self.input_handler = InputHandler(main)
        self.exit = False

    def start(self):
        self.cli_thread = BetterThread(target=self.cli_function)

        self.cli_thread.start()
        #Thread.join(self.cli_thread)

    def cli_function(self):
        while not self.exit:
            input_value = input("> ")
            self.input_handler.handle_input(input_value.strip(" "))
