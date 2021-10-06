from os import path
import psutil

from helpers.window_helper import WindowHelper

class StartupHandler():
    def __init__(self, cache_dir) -> None:
        self.cache_dir = cache_dir
        self.window_helper = WindowHelper()

    def main(self):
        if self._program_is_running():
            with open(self.cache_dir + "hWndfile.txt", "r+") as hWndfile:
                hWnd = int(hWndfile.readline())
                self.window_helper.show_cli(hWnd)
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
            hWndfile.write(str(WindowHelper.get_console_hWnd()))
        with open(self.cache_dir + "pidfile.txt", "w+") as pidfile:
            for p in psutil.process_iter():
                if "cmd.exe" == p.name():
                    pidfile.write(str(p.pid))
