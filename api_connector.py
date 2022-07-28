import socket
import threading
from ToDoList import robotmain
class api_connector:

    def __init__(self):
        thread = threading.Thread(target=robotmain, name='Main GUI thread')
        thread.start()
        self.IP = '127.0.0.1'
        self.PORT = 12345
        self.SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SOCK.connect(('localhost',50000))
    def send_keyword(self,keyword) -> str:
        self.SOCK.sendall(bytes(keyword,'utf-8'))
        try:
            data = self.SOCK.recv(1024)
        except ConnectionResetError:
            return None
        return str(data,'utf-8')

    def send_keyword_args(self,keyword : str,args : str) -> str:
        built = keyword + ' ' + args
        self.SOCK.sendall(bytes(built,'utf-8'))
        data = self.SOCK.recv(1024)
        return str(data,'utf-8')
    def get_result(self) -> str:
        data = self.SOCK.recv(1024)
        return str(data,'utf-8')

if __name__ == '__main__':
    api = api_connector()
    api.send_keyword('quit_program')

