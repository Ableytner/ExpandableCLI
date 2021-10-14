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
            _ = system("cls")
        else:
            _ = system("clear")

    @classmethod
    def get_console_hWnd(cls):
        return windll.kernel32.GetConsoleWindow()

    def background_program_running(self):
        if self._program_is_running():
            with open(config_helper.get_setting("path") + "hWndfile.txt", "r+") as hWndfile:
                hWnd = int(hWndfile.readline())
                self.show_cli(hWnd)
                return False

        self._save_new_values()
        return True

    def _program_is_running(self):
        if path.exists(config_helper.get_setting("path") + "pidfile.txt"):
            with open(config_helper.get_setting("path") + "pidfile.txt", "r") as pidfile:
                pidnumber = int(pidfile.readline())

                if psutil.pid_exists(pidnumber):
                    return True

        return False

    def _save_new_values(self):
        with open(config_helper.get_setting("path") + "hWndfile.txt", "w+") as hWndfile:
            hWndfile.write(str(self.get_console_hWnd()))
        with open(config_helper.get_setting("path") + "pidfile.txt", "w+") as pidfile:
            for p in psutil.process_iter():
                if "cmd.exe" == p.name():
                    pidfile.write(str(p.pid))
