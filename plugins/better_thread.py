from threading import Thread, Event

from plugins.info_module_base import InfoModuleBase

class BetterThread(Thread, InfoModuleBase):
    def __init__(self, *args, **kwargs):
        super(BetterThread, self).__init__(*args, **kwargs)
        self._stop = Event()

    def get_modulename(self):
        return "better_thread"

    def depends_on(self):
        return []

    def get_info(self):
        return super().get_info()

    def get_info_raw(self):
        return super().get_info_raw()

    def start(self) -> None:
        return super().start()

    def execute(self, command):
        return super().execute(command)

    def exit(self):
        return self._stop.set()

    def stopped(self):
        return self._stop.isSet()
