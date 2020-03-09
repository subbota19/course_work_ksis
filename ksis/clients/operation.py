import sys, os, socket

BUFFER_SIZE = 4096


class ClientOperation:

    def __init__(self, sock):
        self.sock = sock
        self.dict_with_operation = {'su': self.operation_su, 'si': self.operation_si, 'al': self.operation_al,
                                    'ad': self.operation_ad, 'ex': self.operation_ex, 'dl': self.operation_dl,
                                    'qt': self.operation_qt, 'hi': self.operation_hi}
        self.active_username = None

    def operation_hi(self):
        self.sock.socket_send('hi')
        print(self.sock.socket_recv(BUFFER_SIZE))

    def operation_si(self):
        username = input('please input username:')
        password = input('please input password:')
        self.sock.socket_send("si username:{} password:{}".format(username, password))
        server_message = self.sock.socket_recv()
        if server_message == 'successful authentication':
            self.active_username = username
        print(server_message)

    def operation_su(self):
        username = input('please input username:')
        password = input('please input password:')
        self.sock.socket_send("su username:{} password:{}".format(username, password))
        server_message = self.sock.socket_recv()
        if server_message == 'successful registration':
            self.active_username = username
        print(server_message)

    def operation_ad(self):
        try:
            file = open(input('input full path to file which you want to add:'), 'r')
        except FileNotFoundError:
            print('file with this path not found')
            return None
        except SyntaxError:
            print('please make correct you request')
            return None
        else:
            self.sock.socket_send('ad active_username:{} file_name:{}'.format(self.active_username, file.name))
            server_message = self.sock.socket_recv()
            if server_message == 'ok':
                while True:
                    data = file.read(BUFFER_SIZE)
                    self.sock.socket_send(data)
                    if not data:
                        break
            print(server_message)
            file.close()

    def operation_qt(self):
        self.sock.socket_close()
        sys.exit()

    def operation_dl(self):
        file_name = input('input file name (with file expansion):')
        self.sock.socket_send('dl active_username:{} file_name:{}'.format(self.active_username, file_name))
        print(self.sock.socket_recv(BUFFER_SIZE))

    def operation_al(self):
        self.sock.socket_send('al active_username:{}'.format(self.active_username))
        print(self.sock.socket_recv())

    def operation_ex(self):
        file_name = input('input file name (with file expansion):')
        kept_path = input('input full path to directory where you want kept file:')
        self.sock.socket_send('ex active_username:{} file_name:{}'.format(self.active_username, file_name))
        file = ''
        try:
            file = open('{}/{}'.format(kept_path, file_name), 'w')
        except FileNotFoundError:
            print('please input correct path')
        server_answer = self.sock.socket_recv()
        if server_answer == 'ok':
            while True:
                data = ''
                try:
                    data = self.sock.socket_recv()
                except socket.timeout:
                    break
                finally:
                    file.write(data)
        file.close()
        print(server_answer)

    @staticmethod
    def get_file_size(file):
        return os.path.getsize(file)
