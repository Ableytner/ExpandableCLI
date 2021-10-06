from os import system, name, path
import psutil

from ctypes import windll, WinDLL

class WindowHelper():
    def __init__(self, cache_dir = None) -> None:
        self.user32 = WinDLL('user32', use_last_error=True)
        self.cache_dir = cache_dir
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
            with open(self.cache_dir + "hWndfile.txt", "r+") as hWndfile:
                hWnd = int(hWndfile.readline())
                self.show_cli(hWnd)
                return False

        self._save_new_values()
        return True

    def _program_is_running(self):
        if path.exists(self.cache_dir + "pidfile.txt"):
            with open(self.cache_dir + "pidfile.txt", "r") as pidfile:
                pidnumber = int(pidfile.readline())

                if psutil.pid_exists(pidnumber):
                    return True

        return False

    def _save_new_values(self):
        with open(self.cache_dir + "hWndfile.txt", "w+") as hWndfile:
            hWndfile.write(str(self.get_console_hWnd()))
        with open(self.cache_dir + "pidfile.txt", "w+") as pidfile:
            for p in psutil.process_iter():
                if "cmd.exe" == p.name():
                    pidfile.write(str(p.pid))
