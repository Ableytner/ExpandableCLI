from dataclasses import dataclass
from types import MethodType
from typing import List

from plugins.better_thread import BetterThread
from plugins.info_module_base import InfoModuleBase
from plugins.average_time import AverageTime

@dataclass
class Plugin:
    inst: InfoModuleBase
    get_modulename: MethodType
    depends_on: MethodType
    get_info: MethodType
    get_info_raw: MethodType
    start: MethodType
    execute: MethodType

class PluginHelper():
    def __init__(self) -> None:
        self.plugin_list: List[Plugin] = []
        self.plugin_list2: List[Plugin] = []

    def load_plugins(self):
        self._load(BetterThread)
        self._load(AverageTime)

    def check_comp(self):
        for plugin_to_check in self.plugin_list:
            depends_on = plugin_to_check["depends_on"](plugin_to_check["inst"])
            for counter, item in enumerate(depends_on):
                compatable = False
                for plugin_to_check_with in self.plugin_list:
                    print(plugin_to_check_with["get_modulename"](plugin_to_check_with["inst"]))
                    if plugin_to_check_with["get_modulename"](plugin_to_check_with["inst"]) == item:
                        compatable = True
                if not compatable:
                    print("Critical error: Plugin " + plugin_to_check["get_modulename"](plugin_to_check["inst"]) + " depends on plugins " + str(depends_on) + "!")
                    exit()

        for plugin_to_check in self.plugin_list2:
            for counter, item in enumerate(plugin_to_check.inst.depends_on()):
                compatable = False
                for plugin_to_check_with in self.plugin_list2:
                    if plugin_to_check_with.inst.get_modulename() == item:
                        compatable = True
                if not compatable:
                    print("Critical error: Plugin " + plugin_to_check.inst.get_modulename() + " depends on plugins " + str(plugin_to_check.inst.depends_on()) + "!")
                    exit()

    def start_plugins(self):
        for plugin in self.plugin_list:
            plugin["start"](plugin["inst"])

    def _load(self, plugin_class: InfoModuleBase):
        plugin_dict = {"inst" : plugin_class(), "get_modulename" : plugin_class.get_modulename, "depends_on" : plugin_class.depends_on, "get_info" : plugin_class.get_info, "get_info_raw" : plugin_class.get_info_raw, "start" : plugin_class.start, "execute" : plugin_class.execute}
        plugin = Plugin(plugin_class(), plugin_class.get_modulename, plugin_class.depends_on, plugin_class.get_info, plugin_class.get_info_raw, plugin_class.start, plugin_class.execute)
        self.plugin_list.append(plugin_dict)
        self.plugin_list2.append(plugin)

    def execute(self, command):
        modulename = command.split(" ")[0]

        if command.split(" ")[1] == "help":
            for plugin in self.plugin_list:
                if plugin["get_modulename"](plugin["inst"]) == modulename:
                    return plugin["get_info"](command.split(" ")[1])
            return None

        for plugin in self.plugin_list:
            if plugin["get_modulename"](plugin["inst"]) == modulename:
                return plugin["execute"](plugin["inst"], command.split(" ")[1])

        print("Plugin " + modulename + " can't be found!")
        print(modulename)
        print(self.plugin_list)
        return None
