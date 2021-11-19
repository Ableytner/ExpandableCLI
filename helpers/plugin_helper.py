import sys
import os.path
from dataclasses import dataclass
from types import MethodType
from typing import List

from core.logging import log, LoggingType
from plugins.base_plugin import BasePlugin

sys.path.insert(1, __file__.rsplit("\\", 2)[0] + "\plugins")

@dataclass
class Plugin:
    inst: BasePlugin
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
        # generates and imports a list of all found plugins
        plugins = self._gen_plugins()
        for plugin in plugins:
            # inits every plugin
            self._init(plugin)

    def check_comp(self):
        # checks if all depends-on of every plugin is satisfied
        # loops through every plugin
        for plugin_to_check in self.plugin_list:
            # loops through every item fo depends_on
            for _, item in enumerate(plugin_to_check.inst.depends_on()):
                compatable = False
                for plugin_to_check_with in self.plugin_list:
                    if plugin_to_check_with.inst.get_pluginname() == item:
                        compatable = True
                # if at least one depends_on isn't satisfied, throw an critical error and exit
                if not compatable:
                    log(__file__, "Critical error: Plugin " + plugin_to_check.inst.get_pluginname() + " depends on plugins " + str(plugin_to_check.inst.depends_on()) + "!", LoggingType.critical, True)
                    exit()
        log(__file__, "Successfully finished plugin compatibility check")

    def startup_plugins(self):
        # only starts al plugins that need to be started on startup
        for plugin in self.plugin_list:
            self._startup(plugin)

    def start_plugins(self):
        # starts all plugins
        for plugin in self.plugin_list:
            self._start(plugin)

    def execute(self, command):
        # passes the given command to the correct plugin

        if command.split(" ")[0] == "help":
            # if the first word is help, assume that the second word is the pluginname
            pluginname = command.split(" ")[1]
        else:
            # assume that the first word is the pluginname
            pluginname = command.split(" ")[0]

        if command.split(" ")[0] == "help" or command.split(" ")[1] == "help":
            for plugin in self.plugin_list:
                if plugin.inst.get_pluginname() == pluginname:
                    # finds the matching plugin and prints its helptext
                    print(plugin.inst.get_info())
                    return

        for plugin in self.plugin_list:
            if plugin.inst.get_pluginname() == pluginname:
                # finds the matching plugin and passes the command to it
                plugin.inst.execute(command.split(" ", maxsplit=1)[1])
                return

        # print a warning if the plugin can't be found
        log(__file__, "Plugin " + pluginname + " can't be found!", LoggingType.warning, printout=True)
        return

    def exit_plugins(self):
        # exits all plugins, waiting auntil everyone has finished exiting
        for plugin in self.plugin_list:
            # sets the _started value of the plugin to false to make it appear as not started
            plugin.inst._started = False
            plugin.inst.exit()
            log(__file__, "Successfully exited plugin " + plugin.inst.get_pluginname(), printout=False)
        # clears the plugin list
        self.plugin_list.clear()

    def disable_plugin(self, pluginname):
        # disables the given plugin
        plugindir = __file__.rsplit("\\", 2)[0] + "\plugins"
        for file in os.listdir(plugindir):
            # loops through every file in the plugins folder
            if file == pluginname + ".py.dis":
                # if the plugin is already disabled, do nothing
                return
            if file == pluginname + ".py":
                # if the plugin isn't already disabled, disable it
                os.rename(plugindir + "\\" + pluginname + ".py", plugindir + "\\" + pluginname + ".py.dis")
                return

        # print a warning if the plugin can't be found
        log(__file__, "Plugin " + pluginname + " can't be found!", LoggingType.warning, printout=True)

    def enable_plugin(self, plugin_name):
        # enables the given plugin
        plugindir = __file__.rsplit("\\", 2)[0] + "\plugins"
        for file in os.listdir(plugindir):
            # loops through every file in the plugins folder
            if file == plugin_name + ".py":
                # if the plugin is already enabled, do nothing
                return
            if file == plugin_name + ".py.dis":
                # if the plugin isn't already enabled, enable it
                os.rename(plugindir + "\\" + plugin_name + ".py.dis", plugindir + "\\" + plugin_name + ".py")
                return

        # print a warning if the plugin can't be found
        print("Plugin " + plugin_name + " can't be found!")

    def print_plugins(self):
        # prints out all plugins and their state (running, stopped or disabled)
        plugins = self.plugin_list.copy() + self._gen_disabled_plugins()
        log(__file__, "Printing " + str(len(plugins)) + " plugins: ", printout=True)
        for plugin in plugins:
            if type(plugin) == str:
                text = plugin + " " * (20 - len(plugin)) + "disabled"
            else:
                text = plugin.inst.get_pluginname() + " " * (20 - len(plugin.inst.get_pluginname()))
                if plugin.inst._started:
                    text += "running"
                else:
                    text += "stopped"
            log(__file__, text, printout=True)

    def _gen_plugins(self):
        # generates a list of all found plugins and imports them
        modulepaths = []
        for file in os.listdir(__file__.rsplit("\\", 2)[0] + "\plugins"):
            if file.startswith("_") or file.endswith(".py.dis") or file == "base_plugin.py":
                # ignore all files that start with _ (all python temp files)
                # also ignore all disabled files, which end with .py.dis, and the base_plugin
                pass
            else:
                # appends all files to a list
                modulepaths.append(file)

        classnames = []
        for file in modulepaths:
            with open(__file__.rsplit("\\", 2)[0] + "\plugins\\" + file, "r") as f:
                # opens every plugin file
                for line in f.readlines():
                    if "class" in line:
                        # saves the classname as a string for every found plugin
                        classnames.append(line.split("class ")[1].split("(")[0])

        plugins = []
        for c in range(len(modulepaths)):
            # imports every found plugin as a module
            module = __import__(modulepaths[c].split(".")[0])
            # gets the class of every plugin and appends it to the plugins list
            plugins.append(getattr(module, classnames[c]))

        return plugins

    def _gen_disabled_plugins(self):
        # generates a list of all found disabled plugins
        dis_plugins = []
        for file in os.listdir(__file__.rsplit("\\", 2)[0] + "\plugins"):
            if file.endswith(".py.dis") and not file.startswith("_") and not file == "base_plugin.py":
                # ignore all files that start with _ (all python temp files)
                # also ignore the base_plugin
                dis_plugins.append(file.split(".")[0])

        return dis_plugins

    def _init(self, plugin_class: BasePlugin):
        # instantiates the given plugin
        plugin = Plugin(plugin_class(), plugin_class.get_pluginname, plugin_class.depends_on, plugin_class.get_info, plugin_class.start, plugin_class.execute, plugin_class.exit, plugin_class.needs_startup)
        # appends the plugin instance to the plugin_list
        self.plugin_list.append(plugin)
        log(__file__, "Successfully initialized plugin " + plugin.inst.get_pluginname())

    def _startup(self, plugin):
        # starts only those plugins that have needs_startup set to true and haven't been started yet
        if plugin.inst.needs_startup() and not plugin.inst._started:
            plugin.inst.start()
            plugin.inst._started = True
            log(__file__, "Successfully started plugin " + plugin.inst.get_pluginname())

    def _start(self, plugin):
        # starts all plugins that haven't been started yet
        if not plugin.inst._started:
            plugin.inst.start()
            plugin.inst._started = True
            log(__file__, "Successfully started plugin " + plugin.inst.get_pluginname())
