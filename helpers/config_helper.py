import json

filepath = "D:\AverageActiveTime\settings.json"

def get_setting(key):
    with open(filepath, "r+") as settingsfile:
        settings = json.load(settingsfile)
        return settings[key]

def get_settings():
    with open(filepath, "r+") as settingsfile:
        return json.load(settingsfile)

def save_setting(key, value):
    try:
        with open(filepath, "r+") as settingsfile:
            settings = json.load(settingsfile)
    except:
        with open(filepath, "w+"):
            pass
        settings = {}
    settings[key] = value
    with open(filepath, "w") as settingsfile:
        json.dump(settings, settingsfile)

# init path into config
try:
    with open(filepath, "r+") as settingsfile:
        settings = json.load(settingsfile)
    if settings == None:
        settings = {}
except:
    with open(filepath, "w+"):
        pass
    settings = {}

settings["path"] = filepath

with open(filepath, "w") as settingsfile:
    json.dump(settings, settingsfile)
