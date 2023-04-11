import struct
import sys

from PyQt5.QtCore import QByteArray, QDataStream, QObject, pyqtSignal, QVariant, pyqtSlot
from PyQt5.QtNetwork import QTcpSocket, QAbstractSocket, QTcpServer, QHostAddress


class Connection(QObject):
    socket: QTcpSocket
    package_size = -1

    def __init__(self):
        super().__init__()
        self.socket = QTcpSocket()
        self.socket.setSocketOption(QTcpSocket.KeepAliveOption, QVariant(1))

    def connect_to_host(self, address: QHostAddress = QHostAddress.LocalHost, port: int = 8080):
        self.socket.connectToHost(address, port)

        if not self.socket.waitForConnected(1000):
            raise Exception('failed to connect')

    def check_connection(self):
        if self.socket.state() != QTcpSocket.ConnectedState:
            print('socket is not connected')
            return False
        return True

    # TODO implement
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

    def read_sent_data(self):
        if self.socket.bytesAvailable() >= sys.getsizeof(int) and self.package_size == -1:
            buffer = QDataStream(self.socket)
            self.package_size = buffer.readUInt32()

        if self.socket.bytesAvailable() < self.package_size:
            return

        buffer = QDataStream(self.socket)
        data = QByteArray()
        buffer >> data
        self.package_size = -1
        return data


class ClientConnection(Connection):
    def __init__(self):
        super().__init__()
        self.socket.readyRead.connect(self.handle_data)
        self.socket.errorOccurred.connect(lambda: print(self.socket.errorString()))
        self.socket.connected.connect(lambda: print("connected to socket"))
        self.socket.disconnected.connect(self.__on_disconnected)

    def handle_data(self):
        msg = self.__read_message()
        print('message command: ' + str(msg.command))

    def __on_disconnected(self):
        print("server disconnected")

    def __read_message(self):
        sent_data = self.read_sent_data()
        sent_data_stream = QDataStream(sent_data)
        msg = self.Message()
        data = self.__get_data(sent_data_stream)
        stream = QDataStream(data)
        msg.read_command(stream)

        return msg

    def __get_data(self, stream: QDataStream) -> QByteArray:
        length = stream.readUInt32()
        return QByteArray(stream.readRawData(length))

    class Message:
        command: int
        payload: QByteArray

        def __init__(self):
            self.command = 0
            self.payload = QByteArray()

        def read_command(self, stream: QDataStream):
            self.command = stream.readUInt32()

