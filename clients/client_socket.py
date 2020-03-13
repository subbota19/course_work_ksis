import socket


class ClientSocket:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def socket_connect(self, tuple_address_port=('127.0.0.1', 8001)):
        self.sock.connect(tuple_address_port)
        self.sock.settimeout(5)

    def socket_send(self, text, add_info=''):
        if add_info:
            text += add_info
        self.sock.send(text.encode('utf-8'))

    def socket_recv(self, size=4096):
        return self.sock.recv(size).decode('utf-8')

    def socket_close(self):
        self.sock.close()
