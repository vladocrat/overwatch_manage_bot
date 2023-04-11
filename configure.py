import configparser
from aenum import Enum


class Config(Enum):
    Bot = 0
    Network = 1


class BotConfig:

    def __init__(self, token, prefix):
        self.token = token
        self.prefix = prefix


class NetworkConfig:

    def __init__(self, address, port):
        self.address = address
        self.port = port


class Configurer:
    def __init__(self, file_path):
        self.config = configparser.ConfigParser()
        self.file_path = file_path

    def configure(self, cfg_type: Config):
        self.config.read(self.file_path)

        if cfg_type == Config.Bot:
            return BotConfig(self.config["Bot"]["token"],
                             self.config["Bot"]["prefix"])
        elif cfg_type == Config.Network:
            return NetworkConfig(self.config["Network"]["address"],
                                 self.config["Network"]["port"])
