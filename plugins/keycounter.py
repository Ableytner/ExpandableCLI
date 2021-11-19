import json
from pynput import keyboard

import helpers.config_helper as config_helper
from plugins.base_plugin import BasePlugin

class KeyCounter(BasePlugin):
    def __init__(self) -> None:
        super().__init__()
        config_helper.save_setting("keycounter.count", 5)
        self.keys = {"-" : 0, "." : 0, "," : 0, "m" : 0, "n" : 0, "b" : 0, "v" : 0, "c" : 0, "x" : 0, "y" : 0, "<" : 0, ">" : 0, "|" : 0, "^" : 0, "°" : 0, "a" : 0, "s" : 0, "d" : 0, "f" : 0, "g" : 0, "h" : 0, "j" : 0, "k" : 0, "l" : 0, "ö" : 0, "ä" : 0, "#" : 0, "+" : 0, "ü" : 0, "p" : 0, "o" : 0, "i" : 0, "u" : 0, "z" : 0, "t" : 0, "r" : 0, "e" : 0, "w" : 0, "q" : 0, "^" : 0, "1" : 0, "2" : 0, "3" : 0, "4" : 0, "5" : 0, "6" : 0, "7" : 0, "8" : 0, "9" : 0, "0" : 0, "ß" : 0, "!" : 0, '"' : 0, "§" : 0, "$" : 0, "%" : 0, "&" : 0, "/" : 0, "(" : 0, ")" : 0, "=" : 0, "?" : 0, "`" : 0, "´" : 0, "{" : 0, "[" : 0, "]" : 0, "}" : 0, "\\" : 0, "+" : 0, "#" : 0, ";" : 0, ":" : 0, "_" : 0, "*" : 0, "'" : 0, "~" : 0, "@" : 0, "€" : 0, "Key.alt" : 0, "Key.alt_gr" : 0, "Key.alt_l" : 0, "Key.alt_r" : 0, "Key.backspace" : 0, "Key.caps_lock" : 0, "Key.cmd" : 0, "Key.cmd_l" : 0, "Key.cmd_r" : 0, "Key.ctrl" : 0, "Key.ctrl_l" : 0, "Key.ctrl_r" : 0, "Key.delete" : 0, "Key.down" : 0, "Key.end" : 0, "Key.enter" : 0, "Key.esc" : 0, "Key.home" : 0, "Key.insert" : 0,  "Key.left" : 0, "Key.menu" : 0, "Key.num_lock" : 0, "Key.page_down" : 0, "Key.page_up" : 0, "Key.pause" : 0, "Key.print_screen" : 0,  "Key.right" : 0, "Key.scroll_lock" : 0, "Key.shift" : 0, "Key.shift_l" : 0, "Key.shift_r" : 0, "Key.space" : 0, "Key.tab" : 0, "Key.up" : 0, "Key.f1" : 0, "Key.f2" : 0, "Key.f3" : 0, "Key.f4" : 0, "Key.f5" : 0, "Key.f6" : 0, "Key.f7" : 0, "Key.f8" : 0, "Key.f9" : 0, "Key.f10" : 0, "Key.f11" : 0, "Key.f12" : 0}
        try:
            with open(config_helper.get_setting("path") + "keycounter.keys.json", 'r+') as jsonfile:
                tempkeys = json.load(jsonfile)
                if(tempkeys == None) or (tempkeys == {}):
                    pass
                else:
                    self.keys = tempkeys
        except:
            with open(config_helper.get_setting("path") + "keycounter.keys.json", 'w+') as save:
                json.dump(self.keys, save)

    def get_pluginname(self):
        return "keycounter"

    def needs_startup(self):
        return True

    def get_info(self):
        helptext = ""

        helptext += "Showing help for the keycounter plugin:\n"
        helptext += f"list --> Shows the top {config_helper.get_setting('keycounter.count')} pressed keys\n"
        helptext += "list-all --> Shows all pressed keys, sorted by the amount of times pressed\n"
        helptext += "count [n] --> Changes the amount of keys displayed by 'list'"

        return helptext

    def start(self):
        super().start()

        self.listener = keyboard.Listener(
            on_press=self.on_press,
        )
        self.listener.start()

    def execute(self, command):
        if command == "list":
            self.print_n(config_helper.get_setting("keycounter.count"))
        elif command == "list-all":
            self.print_all()
        elif command.split(" ")[0] == "count":
            try:
                count_value = int(command.split(" ")[1])
                config_helper.save_setting("keycounter.count", count_value)
            except:
                print(f"Unknown value {command.split(' ')[1::]}")
        else:
            print("Unknown command " + command + "!")

    def exit(self):
        self.listener.stop()
        print("stopped logging keystrokes --> closing program")

    def print_n(self, count):
        with open(config_helper.get_setting("path") + "keycounter.keys.json", "r+") as jsonfile:
            tempkeys = json.load(jsonfile)
        sortkeys = dict(sorted(tempkeys.items(), key=lambda item: item[1], reverse=True))
        counter = 0
        for key in sortkeys:
            if(counter <= count):
                print("[", key.replace("Key.", ""), "]", ": ", sortkeys[key]) 
            counter += 1

    def print_all(self):
        with open(config_helper.get_setting("path") + "keycounter.keys.json", "r+") as jsonfile:
            tempkeys = json.load(jsonfile)
        sortkeys = dict(sorted(tempkeys.items(), key=lambda item: item[1], reverse=True))
        for key in sortkeys:
            print("[", key.replace("Key.", ""), "]", ": ", sortkeys[key]) 

    @staticmethod
    def get_char(key):
        try:
            return key.char
        except AttributeError:
            return str(key)

    def on_press(self, key):
        try:
            self.keys[self.get_char(key)] += 1
            with open(config_helper.get_setting("path") + "keycounter.keys.json", 'w+') as save:
                json.dump(self.keys, save)
        except:
            pass
