from aenum import Enum


class Protocol(Enum):
    class Server(Enum):
        hello = 0

    class Client(Enum):
        hello = 0

    class Bot(Enum):
        hello = 256
