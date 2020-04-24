from servers.cache import Cache
from models.model import User, db_connection
from servers.create_yaml_file import create_file, check_client
import re, os, socket

BUF_SIZE = 4096

PATH = '/home/zhenya/PycharmProjects/Pyramid/ksis/files'

INSTRUCTION = """
    hi and welcome to our program file sharing.
    for further cooperation you must follow next instructions:
    *all commands input in accordance with next phrases
    su-sign up(registration)
    si-sign in(authentication)
    al-watch all available files
    ad file_name-add file
    ex full_name-extract file
    dl full_name-delete file
    qt-quit
"""


class ServerOperation:

    def __init__(self, sock):
        self.sock = sock
        self.cache_obj = Cache()
        self.dict_with_operation = {'su': self.operation_su, 'si': self.operation_si, 'al': self.operation_al,
                                    'ad': self.operation_ad, 'dl': self.operation_dl, 'ex': self.operation_ex,
                                    'hi': self.hello}

    def hello(self, client, full_command_name):
        client.send(self.encode_message(INSTRUCTION))

    def operation_si(self, client, full_command_name):
        password = self.re_find_password(full_command_name)
        username = self.re_find_username(full_command_name)

        if not password or not username:
            client.send(self.encode_message('please input correct username and password'))
            return None

        if check_client(username, password, PATH):
            self.cache_obj.cache_set(username, True)
            client.send(self.encode_message('successful authentication'))
            return None
        client.send(self.encode_message('unsuccessful authentication'))

    def operation_su(self, client, full_command_name):
        session = db_connection.session()
        password = self.re_find_password(full_command_name)
        username = self.re_find_username(full_command_name)

        if not password or not username:
            client.send(self.encode_message('please input correct username and password'))
            return None
        if session.query(User).filter(User.username == username).first():
            client.send(self.encode_message('user with this username {} already exist'.format(username)))
            return None

        session.add(User(username=username, password=password))
        session.commit()

        self.cache_obj.cache_set(username, True)

        os.mkdir('{}/{}'.format(PATH, username))
        create_file(username, password, client, path=PATH)

        client.send(self.encode_message('success registration'))

    def operation_ad(self, client, full_command_name):
        active_user = self.re_find_active_user(full_command_name)
        file_name = self.re_find_file_name(full_command_name)
        if self.cache_obj.cache_get(active_user):
            client.send(self.encode_message('ok'))
        else:
            client.send(self.encode_message('please authorise to submit your command'))
            return None
        file = open('{}/{}/{}'.format(PATH, active_user, file_name), 'w')
        while True:
            data = ''
            try:
                data = self.decode_message(client.recv(BUF_SIZE))
            except socket.timeout:
                break
            finally:
                file.write(data)
        file.close()

    def operation_dl(self, client, full_command_name):
        active_user = self.re_find_active_user(full_command_name)
        file_name = self.re_find_del_file_name(full_command_name)
        if not self.cache_obj.cache_get(active_user):
            client.send(self.encode_message('please authorise to submit your command'))
            return None
        try:
            os.remove('{}/{}/{}'.format(PATH, active_user, file_name))
            client.send(self.encode_message('ok'))
        except FileNotFoundError:
            client.send(self.encode_message("file with this name doesn't exist"))

    def operation_ex(self, client, full_command_name):
        active_user = self.re_find_active_user(full_command_name)
        file_name = self.re_find_del_file_name(full_command_name)
        if not self.cache_obj.cache_get(active_user):
            client.send(self.encode_message('please authorise to submit your command'))
            return None
        try:
            file = open('{}/{}/{}'.format(PATH, active_user, file_name, 'r'))
        except FileNotFoundError:
            client.send(self.encode_message("file with this name doesn't exist"))
        except (SyntaxError, IsADirectoryError):
            client.send(self.encode_message('please make correct you request'))
        else:
            client.send(self.encode_message('ok'))
            while True:
                data = file.read(BUF_SIZE)
                client.send(self.encode_message(data))
                if not data:
                    break
            file.close()

    def operation_al(self, client, full_command_name):
        active_user = self.re_find_active_user(full_command_name)

        if not self.cache_obj.cache_get(active_user):
            client.send(self.encode_message('please authorise to submit your command'))
            return None
        dir_location = os.listdir('{}/{}'.format(PATH, active_user))
        if not dir_location:
            client.send(self.encode_message("you haven't active files in our program"))
            return None
        client.send(self.encode_message(str(dir_location)))

    @staticmethod
    def re_find_password(string):
        password = re.findall(r'password:([\S]+)', string)
        if password:
            return password[0]
        return None

    @staticmethod
    def re_find_username(string):
        username = re.findall(r'username:([\S]+)', string)
        if username:
            return username[0]
        return None

    @staticmethod
    def re_find_active_user(string):
        return re.findall(r'active_username:([\S]+)', string)[0]

    @staticmethod
    def re_find_file_name(string):
        return re.split('/', re.findall(r'file_name:([\S]+)', string)[0])[-1]

    @staticmethod
    def re_find_del_file_name(string):
        try:
            response = re.findall(r'file_name:([\S]+)', string)[0]
        except IndexError:
            response = ''
        finally:
            return response

    @staticmethod
    def re_find_file_size(string):
        return re.findall(r'file_size:([\S]+)', string)[0]

    @staticmethod
    def get_file_size(file):
        return os.path.getsize(file)

    @staticmethod
    def decode_message(message):
        return message.decode('utf-8')

    @staticmethod
    def encode_message(message):
        return message.encode('utf-8')
