from threading import Thread, Event

from plugins.info_module_base import InfoModuleBase

class BetterThread(Thread, InfoModuleBase):
    def __init__(self, *args, **kwargs):
        self._stop = Event()
        super(BetterThread, self).__init__(*args, **kwargs)

    def get_modulename(self):
        return "better_thread"

    def get_info(self):
        return super().get_info()

    def start(self) -> None:
        return super().start()

    def execute(self, command):
        return super().execute(command)

    def exit(self):
        return self._stop.set()

    def stopped(self):
        return self._stop.isSet()
