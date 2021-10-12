import os.path
from datetime import datetime
from enum import Enum

import helpers.config_helper as config_helper

class LoggingType(Enum):
    info = "INFO"
    warning = "WARNUNG"
    error = "ERROR"
    critical = "CRITICAL"

def log(file, logging_type: LoggingType, message):
    if config_helper.get_setting("logging") != True:
        return
    #if not os.path.isfile(config_helper.get_setting("path") + "logfile.txt"):
        #with open(config_helper.get_setting("path") + "logfile.txt", "w+") as f:
            #pass
    log_text = "["
    log_text += str(datetime.now().hour) + ":" + str(datetime.now().minute) + ":" + str(datetime.now().second) + ":" + str(datetime.now().microsecond) + "|"
    log_text += file.split("\\")[-1].split(".")[0] + "|"
    log_text += logging_type.value + "] "
    log_text += message + "\n"

    with open(config_helper.get_setting("path") + "logfile.txt", "a+") as f:
        f.write(log_text)
    print (log_text)
    #print(file.split("\\")[-1].split(".")[0], logging_type.value, message)
