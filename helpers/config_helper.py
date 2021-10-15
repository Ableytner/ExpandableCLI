import json

filepath = "D:\AverageActiveTime\\"

def get_setting(key):
    with open(filepath + "settings.json", "r+") as settingsfile:
        settings = json.load(settingsfile)
        return settings[key]

def get_settings():
    with open(filepath + "settings.json", "r+") as settingsfile:
        return json.load(settingsfile)

def save_setting(key, value):
    try:
        with open(filepath + "settings.json", "r+") as settingsfile:
            settings = json.load(settingsfile)
    except:
        with open(filepath + "settings.json", "w+"):
            pass
        settings = {}
    settings[key] = value
    with open(filepath + "settings.json", "w") as settingsfile:
        json.dump(settings, settingsfile)

# init path into config
try:
    with open(filepath + "settings.json", "r+") as settingsfile:
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
