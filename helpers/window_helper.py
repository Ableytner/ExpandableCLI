from os import system, name

from ctypes import windll, WinDLL

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
