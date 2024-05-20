import json
import os


class ConfigurationManager:
    def __init__(self, filename="config.json"):
        self.filename = filename
        self.config = self.loadConfig()

    def loadConfig(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                config = json.load(file)
                print("Configuration loaded.")
                return config
        print("No configuration file found. Using default settings.")
        return {}

    def saveConfig(self):
        with open(self.filename, "w") as file:
            json.dump(self.config, file, indent=4)
        print("Configuration saved.")

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.saveConfig()
