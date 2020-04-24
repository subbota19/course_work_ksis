import yaml, socket, datetime


def create_file(name, password, sock, path):
    try:
        yaml_file = open('{}/{}/register.yaml'.format(path, name), 'w')
    except FileNotFoundError:
        return None
    yaml.dump({
        'user': {
            'name': name, 'password': password, 'created_time': datetime.datetime.now(),
            'updated_time': datetime.datetime.now()
        },
        'socket': {
            'family': str(sock.family), 'dns_name': socket.gethostbyaddr(sock.getsockname()[0]),
            'server_addr': sock.getsockname(), 'client_addr': sock.getpeername()
        }
    }, yaml_file, Dumper=yaml.Dumper)


def check_client(username, password, path):
    try:
        yaml_file = open('{}/{}/register.yaml'.format(path, username), 'r')
    except FileExistsError:
        return False
    except FileNotFoundError:
        return False
    return yaml.load(yaml_file, Loader=yaml.Loader)['user']['password'] == password
