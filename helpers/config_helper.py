import json

# the filepath to where all config files get saved to
filepath = "D:\ExpandableCLI\\"

def get_setting(key):
    # gets the setting responding for the given key
    with open(filepath + "settings.json", "r+") as settingsfile:
        settings = json.load(settingsfile)
        return settings[key]

def get_settings():
    # returns all saved settings as a dictionary
    with open(filepath + "settings.json", "r+") as settingsfile:
        return json.load(settingsfile)

def save_setting(key, value):
    # saves a new key and value for it
    try:
        # tries to read the config file
        with open(filepath + "settings.json", "r") as settingsfile:
            # reads the settings directory
            settings = json.load(settingsfile)
    except:
        # if an error occurs, assume that the saved settings file is corrupted, and creata a new one
        with open(filepath + "settings.json", "w+"):
            pass
        settings = {}
    settings[key] = value
    with open(filepath + "settings.json", "w") as settingsfile:
        # saves the new settings dictionary
        json.dump(settings, settingsfile)

# init path into config
try:
    with open(filepath + "settings.json", "r") as settingsfile:
        settings = json.load(settingsfile)
    if settings == None:
        settings = {}
except:
    with open(filepath + "settings.json", "w+"):
        pass
    settings = {}

settings["path"] = filepath

with open(filepath + "settings.json", "w") as settingsfile:
    json.dump(settings, settingsfile)
