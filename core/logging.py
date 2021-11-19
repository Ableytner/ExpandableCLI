import os.path
from datetime import datetime
from enum import Enum

import helpers.config_helper as config_helper

class LoggingType(Enum):
    info = "INFO"
    warning = "WARN"
    error = "ERRO"
    critical = "CRIT"

def log(file, message: str, logging_type: LoggingType = LoggingType.info, printout: bool = False, notime: bool = False):
    """
    @brief: method to log a message
            method only writes to the log file if logging is enabled
    @param file: must always be self.__file__, is used to get the class name
    @param message: the message to log, given as a string
    @param logging_type [optional]: the importance of the message, default is LoggingType.info
    @param printout [optional]: if True, will also print the given message on the console, default is False
    @param notime [optional]: if True, will not append a timestamp to the message written in the log file, default is False
    @returns: None
    """

    if printout:
        print(message)

    # if logging is disabled, don't write the message in the log file
    if config_helper.get_setting("logging") != True:
        return

    if not notime:
        # logs the text
        now = datetime.now()
        log_text = "["
        log_text += str(now).replace(" ", "|") + "|"            # the current time
        log_text += file.split("\\")[-1].split(".")[0] + "|"    # the classname
        log_text += logging_type.value + "] "                   # the logging type
        log_text += message + "\n"                              # the message
    else:
        # logs the text without additional info
        log_text = message + "\n"

    with open(config_helper.get_setting("path") + "logfile.txt", "a+") as f:
        f.write(log_text)
