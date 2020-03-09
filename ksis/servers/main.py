import socket

from servers.server_socket import ServerSocket
from servers.operation import ServerOperation

BUF_SIZE = 4096


def main():
    while True:
        client, accept = sock.socket_accept()
        while True:
            try:
                client.settimeout(5)
                operation_message = client.recv(BUF_SIZE).decode('utf-8')
                if not operation_message:
                    break
                operation_obj.dict_with_operation[operation_message[:2]](client, operation_message)
            except KeyError:
                continue
            except socket.timeout:
                continue


if __name__ == "__main__":
    sock = ServerSocket()
    sock.socket_connect()

    operation_obj = ServerOperation(sock)
    main()
