import pickle
import socket
import queue
import zlib

from threading import Thread
from CODE.MAIN.DataClass import *
from CODE.SERVER.DataRead import DataRead

class Server:
    def __init__(self):

        # --초기 값 설정
        self.ServerSocket = None
        self.list_Socket = list()

        self.client: dict[tuple, list[socket.socket, str]] = {}
        self.dict_: dict = {}

        self.port = 3333
        self.listener = 10
        self.format = 'utf-8'

       # --- db 연결
        self.db = DataRead()

        # --- 소켓 생성
        self.init_socket()

    def init_socket(self):
        # 소켓 생성
        self.ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 소켓 연결 때 사용된 주소를 재사용 하도록 함
        self.ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ServerSocket.bind(("", self.port))
        self.ServerSocket.listen(self.listener)
        print(" [ 서버 시작 ] ")

        self.list_Socket.clear()
        self.list_Socket.append(self.ServerSocket)

        # 접속한 클라이언트 정보 key :(ip,포트번호), value : [소켓정보, 아이디]
        self.client: dict[tuple, list[socket.socket, str]] = {}
        print(f"client: {self.client}")

    # 접속한 클라이언트가 있는지 확인한다 -> 클라이언트 전송함수에서 조건문 활용
    def connected(self):
        if len(self.client):
            return True
        else:
            return False

    # 클라이언트 연결 종료
    def disconnect(self, sock):
        """ recevie()내 예외처리 시 연결을 종료시킨다."""

        # 클라이언트의 주소를 얻는 메서드 : getpeername()
        addr = sock.getpeername()
        # 접속 종료한 클라이언트의 정보가 현재접속자 내에 존재한다면
        if addr in self.client:
            # 클라이언트 정보를 삭제한다.
            del self.client[addr]

    def accept(self):
        sock, addr = self.ServerSocket.accept()

        print(" [ 클라이언트 접속 ] ")
        self.client[addr] = [sock, ""]
        print("------------------")

        return sock, addr

    def send(self, sock:socket.socket, data):
        print(" [ 데이터를 클라이언트에게 전송! ] ")

        # 공통 요청회신 : 로그인, 채팅방나가기
        # 사용자 요청회신 : 아이디중복확인, 이메일유효, 회원가입, 사용자예약승인, 사용자 구독요청
        # 관리자 요청회신 : 예약수정, 예약취소, 예약승인용 이메일전송
        if type(data) in [PerLogin,
                          PerDuplicateCheck, PerValidEmail, PerJoin, DeleteChat, PerResOk, PerSubTheme,
                          PerResfix, PerResCancel, PerEmailSend]:
            self.send_client(sock, data)

        # 같은 채팅방 멤버에게만 데이터 전송 : 사용자 채팅, 관리자 채팅
        elif type(data) in [ReqUserChat, ReqMngChat]:
            self.send_message(data)

    # 요청 클라이언트(사용자, 관리자)에게 전송
    def send_client(self, sock: socket.socket, data):
        if self.connected():
            sock.sendall(pickle.dumps(data))
            return True
        else:
            return False

    # 채팅방 멤버(사용자, 관리자)에게 전송
    def send_message(self, data):
        if self.connected():
            if type(data) == ReqUserChat:
                print(" [ 사용자의 채팅 메세지 전송 ] ")

                for idx, client in enumerate(self.client.values()):
                    print(f"client[1] : {client[1]}")
                    print(f" 주석 필요 ! ")
                    if data.user_id != client[1]:
                        client[0].sendall(pickle.dumps(data))

                    # 메세지 발송내역 저장(only once)
                    if idx == 0:
                        self.db.insert_data(data)
                    return True

            if type(data) == ReqMngChat:
                print(" [ 관리자의 채팅 메세지 전송 ] ")

                for idx, client in enumerate(self.client.values()):
                    print(f"client[1] : {client[1]}")
                    print(f" 주석 필요 ! ")
                    if data.manager_id != client[1]:
                        client[0].sendall(pickle.dumps(data))

                    # 메세지 발송내역 저장(only once)
                    if idx == 0:
                        self.db.insert_data(data)
                return True

        # 클라이언트와 연결이 되지 않은 상태
        else:
            return False

    # 발송자를 제외한 나머지 접속자에게 발송
    def send_exclude_sender(self, sock: socket.socket, data):
        if self.connected():
            for idx, client in enumerate(self.client.values()):
                if self.client[sock.getpeername()][1] != client[1]:
                    client[0].sendall(pickle.dumps(data))
            return True

        else:
            return False

    def compress_data(self, data):
        return zlib.compress(data.encode('utf-8'))

    def decompress_data(self, data):
        return zlib.decompress(data).decode('utf-8')

    def recevie(self, sock:socket.socket):
        # 데이터 발송 클라이언트 주소 반환
        try:
            # 클라이언트 소켓으로부터 데이터 수신받기
            recv_message = socket.recv(4096)
            # 데이터 수신 실패시 오류를 발생시킨다.
            if not recv_message:
                print("[ recevie error ]")
                raise

            # 수신 받은 데이터를 변환하여 받환받는다
            data = pickle.loads(recv_message)
            return data

        # 예외상황 발생
        except:
            # 소켓 연결종료
            self.disconnect(sock)
            # 소켓 닫기
            sock.close()
            return None

    def process_data(self, sock, data):
        print("before")
        print(f"process_data : {type(data)}")

        # 사용자 채팅 전송
        if type(data) == ReqUserChat:
            return data

        # 아이디 중복 확인 요청
        elif type(data) == ReqDuplicateCheck:
            perdata: PerDuplicateCheck = self.db.membership_id_check(data)

        # 이메일 유효성 확인
        elif type(data) == ReqValidEmail:
            perdata:  PerValidEmail = self.db.eamil_check(data)

        # 회원가입 요청
        elif type(data) == ReqJoin:
            perdata: PerJoin = self.db.membership_regist(data)

        # 로그인 요청
        elif type(data) == ReqLogin:
            perdata : PerLogin = self.db.login(data)

        # 로그아웃 요청
        # elif type(data) == Logout:
        #     user_id = self.client[sock.getpeername()][1]
        #     self.client[sock.getpeername()][1] = ""

        # 사용자 구독알림 요청
        elif type(data) == ReqSubTheme:
            perdata: PerSubTheme = self.db.save_subtb(data)

        # 사용자 예약확인 요청
        elif type(data) == ReqResUserOK:
            perdata: PerResOk = self.db.save_restb(data)

     #--------------------------------------------------------#

        # 관리자 채팅 전송
        elif type(data) == ReqMngChat:
            return data

        # 관리자 예약승인/구독알림 : 이메일 전송요청
        elif type(data) == ResMngOk:
            perdata: PerEmailSend = self.db.send_email(data)

        # 관리자 예약 수정 요청
        elif type(data) == ReqResFix:
            perdata: PerResfix = self.db.update_restb(data)

        # 관리자 예약 삭제 요청
        elif type(data) == ReqResCancel:
            perdata: PerResCancel = self.db.delete_restb(data)

    def handler(self, sock, queue_: queue.Queue):
        while True:
            data = self.recevie(sock)

            if not data:
                break

            print("[ 데이터 수신중 ]")
            # 수신된 데이터에 따른 결과 반환값을 클라이언트로 보내주기
            print(data)
            # 클라이언트에게 받은 데이터를 Queue에 추가
            queue_.put(data)

            while True:
                try:
                    # Queue에서 데이터 얻기
                    get_data = queue_.get(block=False)
                    process_data = self.process_data(sock, get_data)
                    print("[ 데이터 처리중 ]")
                    self.send(sock, process_data)
                    print("[ 데이터 처리완 ]")
                    queue_.task_done()
                except Exception as e:
                    print(f"Error occurred: {e}")

if __name__ == "__main__":
    server = Server()
    # 데이터를 받을 Queue 추가
    data_queue = queue.Queue(maxsize=100)

    while True:
        print("서버 Watiting..")

        c_sock, c_addr = server.accept()
        c_thread = Thread(target=server.handler, args=(c_sock,data_queue), daemon=True)
        c_thread.start()
