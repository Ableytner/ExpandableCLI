from os import system, name, path
import psutil

from ctypes import windll, WinDLL

import helpers.config_helper as config_helper

class WindowHelper():
    def __init__(self) -> None:
        self.user32 = WinDLL('user32', use_last_error=True)
        self.SW_HIDE = 0
        self.SW_SHOW = 5

    def show_cli(self, hWnd = windll.kernel32.GetConsoleWindow()):
        self.user32.ShowWindow(hWnd, self.SW_SHOW)

    def hide_cli(self, hWnd = windll.kernel32.GetConsoleWindow()):
        self.user32.ShowWindow(hWnd, self.SW_HIDE)

    @classmethod
    def clear(cls):
        if name == "nt":
            # windows
            _ = system("cls")
        else:
            # linux
            _ = system("clear")

    @classmethod
    def get_console_hWnd(cls):
        return windll.kernel32.GetConsoleWindow()

    def background_program_running(self):
        if self._already_running():
            # if a running instance has been discovered
            with open(config_helper.get_setting("path") + "hWndfile.txt", "r+") as hWndfile:
                hWnd = int(hWndfile.readline())
                self.show_cli(hWnd)
                return True

        # if no running instance is discovered
        # save the current hWnd to the file
        self._save_hWnd()
        # save the current pid to the file
        self._save_pid()
        return False

    def _already_running(self):
        try:
            if path.exists(config_helper.get_setting("path") + "pidfile.txt"):
                with open(config_helper.get_setting("path") + "pidfile.txt", "r") as pidfile:
                    pidnumber = int(pidfile.readline())
                    if psutil.pid_exists(pidnumber):
                        return True
            return False
        except:
            # if an exception occurs while reading the pidfile, assert that it is not running
            return False

    def _save_hWnd(self):
        with open(config_helper.get_setting("path") + "hWndfile.txt", "w+") as hWndfile:
            hWndfile.write(str(self.get_console_hWnd()))

    def _save_pid(self):
        with open(config_helper.get_setting("path") + "pidfile.txt", "w+") as pidfile:
            for process in psutil.process_iter():
                if "cmd.exe" == process.name():
                    pidfile.write(str(process.pid))

