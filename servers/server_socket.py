import socket
from threading import Thread

BUF_SIZE = 4096


class ClientThread(Thread):

    def __init__(self, client, operation_obj):
        Thread.__init__(self)
        self.client = client
        self.operation_obj = operation_obj

    def run(self):

        while True:
            try:
                self.client.settimeout(5)
                operation_message = self.client.recv(BUF_SIZE).decode('utf-8')
                if not operation_message:
                    break
                self.operation_obj.dict_with_operation[operation_message[:2]](self.client, operation_message)
            except KeyError:
                continue
            except ConnectionResetError:
                continue
            except socket.timeout:
                continue


class ServerSocket:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def socket_connect(self, tuple_address_port=('127.0.0.1', 8001), number_listen=5):
        self.sock.bind(tuple_address_port)
        self.sock.listen(number_listen)

    def socket_close(self):
        self.sock.close()

    def socket_accept(self):
        return self.sock.accept()
