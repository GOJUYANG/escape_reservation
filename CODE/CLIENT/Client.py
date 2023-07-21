import socket
import pickle
import zlib

class Client:
    def __init__(self, server_ip="10.10.20.104", server_port=3333):
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

    def compress_data(self,data):
        return zlib.compress(data.encode('utf-8'))

    def decompress_data(self, data):
        return zlib.decompress(data).decode('utf-8')

    # 데이터 수신
    def recevie(self):
        try:
            recevie_bytes = self.sock.recv(16184)
            if not recevie_bytes:
                print(" [ 데이터 수신 오류 ] ")

            data = pickle.loads(recevie_bytes)
            print(data)
            return data
        except socket.error:
            self.disconnect()
            return None

    # 데이터 발송
    def send(self, data):
        try:
            compressed_data = self.compress_data(data)
            self.sock.sendall(compressed_data)
            # self.sock.sendall(pickle.dumps(data))
            return True
        except socket.error:
            self.disconnect()
            return False

    # 클라이언트의 어드레스 반환
    def address(self):
        return self.sock.getsockname()