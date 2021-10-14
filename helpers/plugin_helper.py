from dataclasses import dataclass
from types import MethodType
from typing import List

from plugins.info_module_base import InfoModuleBase
from plugins.better_thread import BetterThread
from plugins.average_time import AverageTime
from plugins.keycounter import KeyCounter

@dataclass
class Plugin:
    inst: InfoModuleBase
    get_pluginname: MethodType
    get_info: MethodType
    start: MethodType
    execute: MethodType
    exit: MethodType
    depends_on: MethodType
    needs_startup: MethodType

class PluginHelper():
    def __init__(self) -> None:
        self.plugins = [BetterThread, AverageTime, KeyCounter]
        self.plugin_list: List[Plugin] = []

    def init_plugins(self):
        for plugin in self.plugins:
            self._init(plugin)

    def start_plugins(self):
        for plugin in self.plugin_list:
            plugin.inst.start()

    def exit_plugins(self):
        for plugin in self.plugin_list:
            plugin.inst.exit()

    def check_comp(self):
        for plugin_to_check in self.plugin_list:
            for counter, item in enumerate(plugin_to_check.inst.depends_on()):
                compatable = False
                for plugin_to_check_with in self.plugin_list:
                    if plugin_to_check_with.inst.get_pluginname() == item:
                        compatable = True
                if not compatable:
                    print("Critical error: Plugin " + plugin_to_check.inst.get_pluginname() + " depends on plugins " + str(plugin_to_check.inst.depends_on()) + "!")
                    exit()

    def needs_startup(self):
        for plugin in self.plugin_list:
            if plugin.needs_startup:
                return True
        return False

    def start_startup_plugins(self):
        for plugin in self.plugin_list:
            if plugin.needs_startup:
                plugin.inst.start()

    def _init(self, plugin_class: InfoModuleBase):
        plugin = Plugin(plugin_class(), plugin_class.get_pluginname, plugin_class.depends_on, plugin_class.get_info, plugin_class.start, plugin_class.execute, plugin_class.exit, plugin_class.needs_startup)
        self.plugin_list.append(plugin)

    def execute(self, command):
        pluginname = command.split(" ")[0]

        if command.split(" ")[0] == "help" or command.split(" ")[1] == "help":
            for plugin in self.plugin_list:
                if plugin.inst.get_pluginname() == pluginname:
                    print(plugin.inst.get_info())
                    return
            return None

        for plugin in self.plugin_list:
            if plugin.inst.get_pluginname() == pluginname:
                return plugin.inst.execute(str(command.split(" ")[1::]))

        print("Plugin " + pluginname + " can't be found!")
        return None
