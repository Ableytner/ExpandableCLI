from datetime import datetime
from time import sleep
from threading import Thread
from ctypes import windll, WinDLL
from os import path
import psutil

class Main():
    def __init__(self) -> None:
        self.exit = False
        self.cli_thread = None
        self.update_thread = None
        self.user32 = WinDLL('user32', use_last_error=True)
        self.SW_HIDE = 0
        self.SW_SHOW = 5

    def main(self):
        self.cli_thread = Thread(target=self.cli_function)
        self.update_thread = Thread(target=self.update_function)
        
        if self.program_is_running():
            with open("D:\AverageActiveTime\hWndfile.txt", "r+") as hWndfile:
                hWnd = int(hWndfile.readline())
                self.show_cli(hWnd)
                exit()

        self.save_new_values()

        self.start()

        self.cli_thread.start()
        self.update_thread.start()

        Thread.join(self.cli_thread)

    def program_is_running(self):
        if path.exists("D:\AverageActiveTime\pidfile.txt"):
            with open("D:\AverageActiveTime\pidfile.txt", "r") as pidfile:
                pidnumber = int(pidfile.readline())

                if psutil.pid_exists(pidnumber):
                    return True

        return False

    def save_new_values(self):
        with open("D:\AverageActiveTime\hWndfile.txt", "w+") as hWndfile:
            hWndfile.write(str(windll.kernel32.GetConsoleWindow()))
        with open("D:\AverageActiveTime\pidfile.txt", "w+") as pidfile:
            for p in psutil.process_iter():
                if "cmd.exe" == p.name():
                    pidfile.write(str(p.pid))

    def cli_function(self):
        while not self.exit:
            input_value = input("> ")
            self.handle_input(input_value)

    def update_function(self):
        while True:
            self.update()
            sleep(5)

    def handle_input(self, input_value):
        if input_value == "help":
            print(self.get_helptext())
        elif input_value == "hide":
            print("Hiding...")
            sleep(3)
            self.hide_cli()
        elif input_value == "clear":
            print("Clearing console window...")
            pass
            print("Console window cleared!")
        elif input_value == "average":
            pass

    def start(self):
        timeNow = datetime.now()

        with open("D:\AverageActiveTime\logfile.txt", "a+") as logfile:
            log_text = []
            log_text.append("[" + str(timeNow).split(" ")[0] + "|STARTUP] " + str(timeNow).split(" ")[1] + "\n")
            log_text.append("[" + str(timeNow).split(" ")[0] + "|SHUTOFF] " + str(timeNow).split(" ")[1] + "\n")
            logfile.writelines(log_text)

        #print("Saved new time!")

    def update(self):
        timeNow = datetime.now()

        with open("D:\AverageActiveTime\logfile.txt", "r") as logfile:
            lines = logfile.readlines()

        with open("D:\AverageActiveTime\logfile.txt", "w") as logfile:
            lines[-1] = "[" + str(timeNow).split(" ")[0] + "|SHUTOFF] " + str(timeNow).split(" ")[1] + "\n"

            logfile.writelines(lines)

        #print("Updated time!")

    def format_to_seconds(self, time):
        return float(time[0]) * 3600 + float(time[1]) * 60 + float(time[2])

    def format_to_time(self, seconds):
        minutes = 0
        hours = 0

        while seconds >= 60:
            seconds -= 60
            minutes += 1

        while minutes >= 60:
            minutes -= 60
            hours += 1

        return [hours, minutes, seconds]

    def show_cli(self, hWnd = windll.kernel32.GetConsoleWindow()):
        self.user32.ShowWindow(hWnd, self.SW_SHOW)

    def hide_cli(self, hWnd = windll.kernel32.GetConsoleWindow()):
        self.user32.ShowWindow(hWnd, self.SW_HIDE)

    def get_helptext(self):
        helptext = ""

        helptext += "Showing help for the average_active_time module:\n"
        helptext += "help --> Shows this helptext\n"
        helptext += "hide --> Hides the cli\n"
        helptext += "clear --> Clears the console window\n"
        helptext += "average --> Calculates the average active time"

        return helptext

if __name__ == "__main__":
    Main().main()