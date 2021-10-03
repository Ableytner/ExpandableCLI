from abc import ABC, abstractmethod

class InfoModuleBase(ABC):
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
        pass

    @abstractmethod
    def execute(self, command):
        pass

    def exit(self):
        pass
