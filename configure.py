import configparser

#TODO add another class config and move prefix and token there
class Configurer:
    def __init__(self, file_path):
        self.prefix = None
        self.token = None
        self.config = configparser.ConfigParser()
        self.file_path = file_path

    def configure(self):
        self.config.read(self.file_path)
        self.token = self.config["Connection"]["token"]
        self.prefix = self.config["Connection"]["prefix"]
