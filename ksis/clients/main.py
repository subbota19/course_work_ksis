from clients.client_socket import ClientSocket
from clients.operation import ClientOperation


def main():
    while True:
        operation_obj = ClientOperation(sock)
        print('for next work please input word hi:')
        while True:
            input_info = input('>*>')
            try:
                result = operation_obj.dict_with_operation[input_info]()
            except KeyError:
                print('incorrect operation')


if __name__ == "__main__":
    sock = ClientSocket()
    sock.socket_connect()
    main()
