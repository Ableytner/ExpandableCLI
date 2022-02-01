import os

from base_plugin import BasePlugin
from helpers.window_helper import WindowHelper

class Start(BasePlugin):
    def __init__(self) -> None:
        super().__init__()
        self.user_desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop\\')
        self.all_desktop = os.path.join(os.path.join(os.environ['ALLUSERSPROFILE']), 'Desktop\\')
        print(self.user_desktop)
        print(self.all_desktop)

    def get_pluginname(self):
        return "start"

    def get_info(self):
        return ""

    def start(self):
        return super().start()

    def execute(self, command):
        if command == "all":
            os.popen(self.all_desktop + "Firefox.lnk")
            os.popen(self.user_desktop + "Discord.lnk")
            os.popen(self.user_desktop + "Spotify.lnk")
            os.popen(self.user_desktop + "WhatsApp.lnk")
            os.popen(self.user_desktop + "ElevenClock.lnk")
            os.popen(self.user_desktop + "Wallpaper Engine.url")
            WindowHelper().hide_cli()
        elif command == "valo":
            os.popen(self.all_desktop + "VALORANT.lnk")
        elif command == "genshin":
            os.popen(self.user_desktop + "Genshin Impact.url")
        elif command == "dc":
            os.popen(self.user_desktop + "Discord.lnk")
            WindowHelper().hide_cli()
        elif command == "bg":
            os.popen(self.user_desktop + "ElevenClock.lnk")
            os.popen(self.user_desktop + "Wallpaper Engine.url")
        else:
            print("Unknown command " + command + "!")
