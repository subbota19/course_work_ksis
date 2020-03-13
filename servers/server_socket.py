import socket


class ServerSocket:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def socket_connect(self, tuple_address_port=('127.0.0.1', 8001), number_listen=5):
        self.sock.bind(tuple_address_port)
        self.sock.listen(number_listen)

    def socket_close(self):
        self.sock.close()

    def socket_accept(self):
        return self.sock.accept()
