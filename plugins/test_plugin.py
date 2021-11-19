from plugins.base_plugin import BasePlugin
from core.logging import LoggingType, log

class TestPlugin(BasePlugin):
    def get_pluginname(self):
        return "test_plugin"

    def get_info(self):
        return "Test-Info"

    def start(self):
        super().start()
        print("=====TestPlugin started!=====")

    def execute(self, command):
        if command == "types":
            log(__file__, "info", LoggingType.info)
            log(__file__, "warning", LoggingType.warning)
            log(__file__, "error", LoggingType.error)
            log(__file__, "critical", LoggingType.critical)
            return
        else:
            log(__file__, self.get_pluginname() + " can't execute command " + command + "!", LoggingType.warning, printout=True)
