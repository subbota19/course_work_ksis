from servers.server_socket import ServerSocket
from servers.server_socket import ClientThread
from servers.operation import ServerOperation

if __name__ == "__main__":
    sock = ServerSocket()
    sock.socket_connect()
    while True:
        operation_obj = ServerOperation(sock)
        client, accept = sock.socket_accept()
        thread = ClientThread(client, operation_obj)
        thread.start()
