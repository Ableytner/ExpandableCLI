from core.input_handler import InputHandler
from core.better_thread import BetterThread

class CLIHelper():
    def __init__(self, plugin_helper) -> None:
        self.input_handler = InputHandler(plugin_helper, self)
        self.exit = False
        self.cli_thread = None

    def start(self):
        self.cli_thread = BetterThread(target=self.cli_function)

        self.cli_thread.start()

    def cli_function(self):
        while not self.exit:
            input_value = input("> ")
            # pas the read input to the input handler
            self.input_handler.handle_input(input_value.strip(" "))
