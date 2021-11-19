from threading import Thread, Event

class BetterThread(Thread):
    def __init__(self, *args, **kwargs):
        self._stop = Event()
        super(BetterThread, self).__init__(*args, **kwargs)

    def start(self) -> None:
        return super().start()

    def execute(self, command):
        return super().execute(command)

    def exit(self):
        return self._stop.set()

    def stopped(self):
        return self._stop.isSet()
