from abc import ABC, abstractmethod

class BasePlugin(ABC):
    def __init__(self) -> None:
        self._started = False

    @abstractmethod
    def get_pluginname(self):
        pass

    def depends_on(self):
        return []

    def needs_startup(self):
        return False

    @abstractmethod
    def get_info(self):
        pass

    @abstractmethod
    def start(self):
        self._started = True

    @abstractmethod
    def execute(self, command):
        pass

    def exit(self):
        pass
