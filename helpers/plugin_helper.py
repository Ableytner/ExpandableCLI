import sys
import os.path
from dataclasses import dataclass
from types import MethodType
from typing import List

from core.logging import log, LoggingType
from plugins.info_module_base import InfoModuleBase

sys.path.insert(1, __file__.rsplit("\\", 2)[0] + "\plugins")

modulepaths = []
for file in os.listdir(__file__.rsplit("\\", 2)[0] + "\plugins"):
    if file.startswith("_") or file.endswith(".py.dis") or file == "info_module_base.py":
        pass
    else:
        modulepaths.append(file)

classnames = []
for file in modulepaths:
    with open(__file__.rsplit("\\", 2)[0] + "\plugins\\" + file, "r") as f:
        for line in f.readlines():
            if "class" in line:
                classnames.append(line.split("class ")[1].split("(")[0])

plugins = []
for c in range(len(modulepaths)):
    module = __import__(modulepaths[c].split(".")[0])
    plugins.append(getattr(module, classnames[c]))

del(modulepaths)
del(classnames)

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
        self.plugin_list: List[Plugin] = []

    def init_plugins(self):
        for plugin in plugins:
            self._init(plugin)

    def start_plugins(self):
        for plugin in self.plugin_list:
            self._start(plugin)

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
                    log(__file__, LoggingType.critical, "Critical error: Plugin " + plugin_to_check.inst.get_pluginname() + " depends on plugins " + str(plugin_to_check.inst.depends_on()) + "!", True)
                    exit()
        log(__file__, LoggingType.info, "Successfully finished plugin compatibility check")

    def _init(self, plugin_class: InfoModuleBase):
        plugin = Plugin(plugin_class(), plugin_class.get_pluginname, plugin_class.depends_on, plugin_class.get_info, plugin_class.start, plugin_class.execute, plugin_class.exit, plugin_class.needs_startup)
        self.plugin_list.append(plugin)
        log(__file__, LoggingType.info, "Successfully initialized plugin " + plugin.inst.get_pluginname())

    def _start(self, plugin):
        if plugin.needs_startup:
            plugin.inst.start()
            log(__file__, LoggingType.info, "Successfully started plugin " + plugin.inst.get_pluginname())

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
                return plugin.inst.execute(command.split(" ", maxsplit=1)[1])

        print("Plugin " + pluginname + " can't be found!")
        return None

    def disable_plugin(self, plugin_name):
        plugindir = __file__.rsplit("\\", 2)[0] + "\plugins"
        for file in os.listdir(plugindir):
            if file == plugin_name + ".py.dis":
                return
            if file == plugin_name + ".py":
                os.rename(plugindir + "\\" + plugin_name + ".py", plugindir + "\\" + plugin_name + ".py.dis")
                return
        print("Plugin " + plugin_name + " can't be found!")

    def enable_plugin(self, plugin_name):
        plugindir = __file__.rsplit("\\", 2)[0] + "\plugins"
        for file in os.listdir(plugindir):
            if file == plugin_name + ".py":
                return
            if file == plugin_name + ".py.dis":
                os.rename(plugindir + "\\" + plugin_name + ".py.dis", plugindir + "\\" + plugin_name + ".py")
                return
        print("Plugin " + plugin_name + " can't be found!")
