import sys
from PyQt5.QtCore import QByteArray,QDataStream,QIODevice
from PyQt5.QtWidgets import QApplication,QDialog
from PyQt5.QtNetwork import QHostAddress,QTcpServer

class Server(QDialog):
    def __init__(self):
        super().__init__()
        self.tcpServer = None
        self.PORT =1234
        self.IP_ADDRESS = "127.0.0.1"

    def sessionOpened(self):
        self.tcpServer = QTcpServer(self)
        address = QHostAddress(self.IP_ADDRESS)
        if not self.tcpServer.listen(address,self.PORT):
            print("Can not listen!")
            self.close()
            return
        self.tcpServer.newConnection.connect(self.dealCommunication)

    def dealCommunication(self):
        clientConnection = self.tcpServer.nextPendingConnection() # Get a QTCPSocket from the QTCP Server
        block = QByteArray() # instantiate a QByteArray
        out = QDataStream(block,QIODevice.ReadWrite) #QDataStream class provides serialization of binary data to a QIODevice
        out.setVersion(QDataStream.Qt_5_0) # We are using PyQT5 so set the QDataStream version accordingly
        out.writeUInt16(0)
        message = "Goodbye client!" # this is the message we will sned it could come from a widget
        message = bytes(message,encoding='ascii') # get a byte array of the message encoded appropriately
        out.writeString(message) # now use the QDataStream and write the byte array to it
        out.device().seek(0)
        out.writeUInt16(block.size()-2)
        clientConnection.waitForReadyRead() # wait until the conneciton is ready to read
        response = clientConnection.readAll() # read client data response
        print(str(response,encoding='ascii'))
        clientConnection.disconnected.connect(clientConnection.deleteLater) # get the connection ready for clean up
        clientConnection.write(block) # now send the QByteArray
        clientConnection.disconnectFromHost() # now disconnect connection

if __name__ == "__main__":
    app = QApplication(sys.argv)
    server = Server()
    server.sessionOpened()
    sys.exit(server.exec_())
