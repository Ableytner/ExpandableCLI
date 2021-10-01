from abc import ABC, abstractmethod

class InfoModuleBase(ABC):
    @abstractmethod
    def get_modulename(self):
        pass

    @abstractmethod
    def depends_on(self):
        pass

    @abstractmethod
    def get_info(self):
        pass

    @abstractmethod
    def get_info_raw(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def execute(self, command):
        pass

    @abstractmethod
    def exit(self):
        pass
