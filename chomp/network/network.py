import socket
import json

class NetworkChomp:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_host = False
        self.connected = False
        self.opponent_address = None
        self.client_sock = None

    def host_game(self, port):
        self.sock.bind(('', port))
        self.sock.listen(1)
        self.is_host = True
        return self.sock.getsockname()[0]
        
    def join_game(self, host, port):
        self.sock.connect((host, port))
        self.connected = True
        self.opponent_address = (host, port)
        
    def accept_client(self):
        self.client_sock, addr = self.sock.accept()
        self.connected = True
        self.opponent_address = addr
        return addr
        
    def send_message(self, msg_type, data):
        if not self.connected:
            return False
        try:
            message = json.dumps({"type": msg_type, "data": data})
            if self.is_host:
                self.client_sock.send(message.encode())
            else:
                self.sock.send(message.encode())
            return True
        except:
            self.connected = False
            return False
            
    def receive_message(self):
        if not self.connected:
            return None
        try:
            sock = self.client_sock if self.is_host else self.sock
            data = sock.recv(1024)
            if not data:
                self.connected = False
                return None
            return json.loads(data.decode())
        except:
            self.connected = False
            return None
            
    def close(self):
        if self.client_sock:
            self.client_sock.close()
        self.sock.close()


