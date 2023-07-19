import socket
import pickle

class Client:
    def __init__(self, server_ip="10.10.20.104", server_port=9999):
        self.server_ip = server_ip
        self.server_port = server_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 소켓 닫기
    def disconnect(self):
        self.sock.close()

    # 서버 연결
    def connect(self):
        try:
            self.sock.connect((self.server_ip, self.server_port))
            return True
        except socket.error:
            return False

    # 데이터 수신
    def recevie(self):
        try:
            recevie_bytes = self.sock.recv(4096)
            if not recevie_bytes:
                raise

            data = pickle.loads(recevie_bytes)
            return data
        except socket.error:
            self.disconnect()
            return None

    # 데이터 발송
    def send(self, data):
        try:
            self.sock.sendall(pickle.dumps(data))
            return True
        except socket.error:
            self.disconnect()
            return False

    # 클라이언트의 어드레스 반환
    def address(self):
        return self.sock.getsockname()