import struct
import sys

import PyQt5
from PyQt5 import QtCore
from PyQt5.QtCore import QByteArray, QDataStream
from PyQt5.QtNetwork import QTcpSocket, QAbstractSocket, QTcpServer


class Connection:
    socket: QTcpSocket
    package_size = -1

    def __init__(self):
        self.socket = QTcpSocket()

    def check_connection(self):
        if self.socket.state() != QTcpSocket.ConnectedState:
            print('socket is not connected')
            return False
        return True

    def send_command(self, command):
        return False

    def send(self, command, data):
        if not self.check_connection():
            print('socket is not connected')
            return False

        msg = QByteArray()
        command32 = struct.pack(">I", command)
        msg.append(command32)
        msg.append(data)
        stream = QDataStream(self.socket)
        stream.writeUInt32(msg.size())
        stream.writeBytes(msg)

        if stream.status() == QDataStream.WriteFailed:
            print('stream failed to write to socket')
            return False

        if not self.socket.flush():
            print('failed to flush socket')
            return False

        return True

    def read_data(self, data: QByteArray):
        if self.socket.bytesAvailable() >= sys.getsizeof(int) and self.package_size == -1:
            buffer = QDataStream(self.socket)
            self.package_size = buffer.readInt()

        if self.socket.bytesAvailable() < self.package_size:
            return

        buffer = QDataStream(self.socket)
        data = buffer.readBytes()
        self.package_size = -1

    def read_command(self, buffer: QDataStream):
        return buffer.readInt()


class PendingConnection(Connection):

    def __init__(self):
        super().__init__()
        self.socket.readyRead.connect(self.handle_data)

    class Message:
        command: int
        payload: QByteArray

    def __read_message(self):
        data = QByteArray()
        super().read_data(data)
        stream = QDataStream(data)
        msg = self.Message()
        msg.command = self.read_command(stream)
        return msg

    def handle_data(self):
        msg = self.__read_message()
        print(msg)


class UserConnection(Connection):
    def do(self):
        return False


# class Server(QTcpServer):
#     address = ""
#     port = 0
#     connection: Connection
#     pending_connections = []
#     user_connections = []
#
#     def __init__(self, address, port):
#         super().__init__()
#         self.address = address
#         self.port = port
#
#     def listen(self):
#         if not super().listen(self.address, self.port):
#             print('failed to listen on: ' + str(self))
#         print('listening on: ' + str(self))
#
#     def incomingConnection(self, handle: PyQt5.sip.voidptr) -> None:
#         connection = PendingConnection()
#         self.pending_connections.append(connection)
#         return
