import configparser


class Config:

    def __init__(self, token, prefix):
        self.token = token
        self.prefix = prefix


class Configurer:
    def __init__(self, file_path):
        self.config = configparser.ConfigParser()
        self.file_path = file_path

    def configure(self):
        self.config.read(self.file_path)
        return Config(self.config["Connection"]["token"],
                      self.config["Connection"]["prefix"])
