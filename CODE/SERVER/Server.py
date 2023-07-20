from socket import *
import pickle
import select
import threading

from CODE.SERVER.DataRead import DataRead
from CODE.MAIN.DataClass import *
from CODE.SCREEN.MainWidget import LOGIN, MainWindow

import re

header_split = chr(46) # .
list_split = chr(58) # :

class Server:
    def __init__(self):

        # --- 주소값 설정
        self.ip = '10.10.20.104'
        self.Port = 9999
        self.listener = 10
        self.FORMAT = 'utf-8'

        # --- 초기값 설정
        self.ServerSocket = None
        self.list_Socket = list()
        self.client: dict[tuple, list[socket, str]] = {}
        self.dict_: dict = {}
        self.init_socket()

       # --- db 연결
        self.db = DataRead()

       # --- Mainwindow 연결
        self.login_class = LOGIN()

    def init_socket(self):
        # 소켓 생성
        self.ServerSocket = socket(AF_INET, SOCK_STREAM)
        # 소켓 연결 때 사용된 주소를 재사용 하도록 함
        self.ServerSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        # 서버 주소, 포트번호 저장 : 주의! (튜플)형식이다.
        self.ServerSocket.bind(("", self.Port))
        # 서버 소켓 연결 대기 상태
        self.ServerSocket.listen(self.listener)
        print("서버가 시작되었습니다.")

        # 소켓 리스트 초기화
        self.list_Socket.clear()
        self.list_Socket.append(self.ServerSocket)

        # 접속한 클라이언트 정보 key :(ip,포트번호), value : [소켓정보, 아이디]
        self.client: dict[tuple, list[socket, str]] = {}
        print(self.client)

    def connect(self):
        # 접속한 클라이언트가 있는지 확인
        if len(self.client):
            return True
        else:
            return False

    def disconnect(self, sock):
        # 접속 종료한 클라이언트의 정보가 존재한다면
        addr = sock.getpeername()
        if addr in self.client:
            # 클라이언트 정보 삭제
            del self.client[addr]

    def recv_client(self):
        """Thread 타겟"""
        while True:
            # select.select(self.list_socket, [], [], timeout) : list_socket에 포함된 소켓 내 이벤트 발생을 감시하는 역할. (CCTV)
            # list_socket에 이벤트가 발생하면 해당 문장을 실행한다.
            # read_socket : 수신한 데이터를 가진 소켓
            # write_socket : 블로킹되지 않고 데이터를 전송할 수 있는 소켓
            # read_socket : 예외 상황이 발생한 소켓
            # timeout : select()가 블로킹 되는 최대 시간. 타임아웃 발생 시 빈 리스트를 반환함/ None = 무한대기 블로킹
            read_sockets, write_sockets, except_sockets = select.select(self.list_Socket, [], [], 1)
            for r_socket in read_sockets:
                # 신규 클라이언트 소켓 접속
                if r_socket == self.ServerSocket:
                    c_socket, c_addr = self.ServerSocket.accept()
                    print(f"신규 접속 : {c_addr}")
                    data = self.recv_client_req(c_socket)
                    if data is False:
                        continue
                    self.list_Socket.append(c_socket)
                    self.client[c_socket] = data

                # 이미 접속한 클라이언트의 요청
                else:
                    print(f"접속중임 : {c_addr}")
                    data = self.recv_client_req(r_socket)

                    # data가 유효하지 않다면
                    if data is False:
                        # r_socket은 메모리 정리 및 처리 건너뛰기
                        self.list_Socket.remove(r_socket)
                        del self.client[r_socket]
                        # 다음 소켓의 처리로 넘어간다
                        continue

            # 수신데이터 소켓이 예외상황에 처한 경우
            for r_socket in except_sockets:
                self.list_Socket.remove(r_socket)
                del self.client[r_socket]

    def recv_client_req(self, c_socket: socket):
        try:
            # 클라이언트 소켓으로부터 데이터 수신받기
            recv_message = c_socket.recv(4096)
            print(f"recv_client_req : {recv_message.decode(self.FORMAT)}")

            # 공백 제외한 decode 메세지
            decode_msg = recv_message.decode(self.FORMAT).strip()
            # 명령어
            header = decode_msg.split(header_split)[0]

            # 회원가입
            if header == 'membership':
                body = decode_msg.split(header_split)[1]
                join_data = body.split(list_split)
                tb_name = 'USER'
                result = self.login_class.check_membership_info()
                if result:
                    msg = f'membership{header_split}success'.encode(self.FORMAT)
                    self.send_message(c_socket, msg)
                    # USER 테이블 저장
                    self.dict_['USER_ID'] = join_data[0]
                    self.dict_['USER_PW'] = join_data[1]
                    self.dict_['USER_NM'] = join_data[2]
                    self.dict_['USER_EMAIL'] = join_data[3]
                    self.db.insert_data(tb_name, self.dict_)
                    self.dict_ = {}
                else:
                    msg = f'membership{header_split}fail'.encode(self.FORMAT)
                    self.send_message(c_socket, msg)

            # 아이디 중복 확인
            elif header == 'duple':
                id = decode_msg.split(header_split)[1]
                df = self.db.return_df('USER_ID', 'USER')
                if id in df.USER_ID.tolist():
                    msg = f'duple{header_split}true'.encode(self.FORMAT)
                else:
                    msg = f'duple{header_split}false'.encode(self.FORMAT)
                self.send_message(c_socket, msg)

            elif header == 'manager_login':
                msg = f'login{header_split}success'.encode(self.FORMAT)
                self.send_message(c_socket, msg)

            # 로그인
            elif header == 'user_login':
                body = decode_msg.split(header_split)[1]
                login_data = body.split(list_split)
                user_id, user_pw = login_data
                tb_name = 'USER'

                # USER_ID df
                df = self.db.get_table(tb_name, user_id)
                condition = (df['USER_ID'] == f"{user_id}") & (df['USER_PW'] == f"{user_pw}")
                login_result = df[~condition]
                print(login_result)

                if login_result:
                    msg = f'login{header_split}success'.encode(self.FORMAT)
                    self.send_message(c_socket, msg)
                else:
                    msg = f'login{header_split}fail'.encode(self.FORMAT)
                    self.send_message(c_socket, msg)

            # 유효 이메일 확인
            elif header == 'valid':
                body = decode_msg.split(header_split)[1]
                email_data = body.split(list_split)
                id_, address = email_data
                if re.match(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', id_ + address):
                    msg = f'valid{header_split}true'.encode(self.FORMAT)
                else:
                    msg = f'valid{header_split}false'.encode(self.FORMAT)
                self.send_message(c_socket, msg)

            # 아이디 저장하기 : 구현 후순위
            elif header == 'id_save':
                body = decode_msg.split(header_split)[1]
                user_id, is_save = body.split(list_split)
                tb_name = 'USER'
                self.dict_['ID_SAVE'] = 1
                self.db.insert_data(tb_name, self.dict_, user_id)
                self.dict_ = {}

        except Exception as e:
            # 오류 확인
            print(f"Error occurred: {e}")
            return False

    def send_message(self, c_socket: socket, msg):
        print(f"server_send_message : {msg}")
        self.send(c_socket, msg)

    def run_thread(self):
        recv_thread = threading.Thread(target=self.recv_client)

    # 클라이언트 연결 종료
    # def disconnect(self, sock):
    #     # 접속 종료한 클라이언트의 정보가 존재한다면
    #     addr = sock.getpeername()
    #     if addr in self.client:
    #         # 로그아웃 정보 발송
    #         self.send_exclude_sender(sock, LoginInfo([self.client[addr][1]], False))
    #
    #         # 클라이언트 정보 삭제
    #         del self.client[addr]

    # 데이터 타입에따른 데이터 전송
    def send(self, sock: socket.socket, data):
        print(sock, data)
        print("send!")

        # if sock == ''

        # 같은 채팅방 멤버에게 발송
        # if type(data) in [ReqChat, JoinChat, ReqJoinMember, DeleteTable]:
        #     self.send_message(data)
        #
        # # 요청 클라이언트를 제외한 모든 클라이언트에게 발송
        # if type(data) in [LoginInfo]:
        #     self.send_exclude_sender(sock, data)
        #
        # # 요청한 클라이언트에게 회신
        # elif type(data) in [PerDuplicateCheck, PerEmailSend, PerEmailNumber, PerRegist]:
        #     self.send_client(sock, data)
        #
        # # 친구에게 발송
        # elif type(data) in [PerAcceptFriend, ReqSuggetsFriend]:
        #     self.send_friend(sock, data)
        #
        # elif type(data) in [ReqStateChange]:
        #     self.send_all_client(data)
        #
        # # 클라이언트 로그인 요청 → 두 방식으로 발송해야해서 따로 나눔
        # elif type(data) in [PerLogin]:
        #     # 요청자에게 로그인 결과 발송
        #     self.send_client(sock, data)
        #     self.db_log_inout_state_save(data.rescode)
        #
        #
        #     # 로그인 성공시
        #     # 서버에 로그인 정보 저장, 접속자 제외한 클라이언트에게 접속 정보 발송
        #     if data.rescode == 2:
        #         self.client[sock.getpeername()][1] = data.user_id_
        #         self.send_exclude_sender(sock, LoginInfo(data.user_id_))
        # elif type(data) in [ReqMembership]:

    # 친구에게 발송
    # def send_friend(self, sock:socket.socket, data):
    #     if self.connected():
    #         user_id = self.client[sock.getpeername()][1]
    #         print(f"user_id : {user_id}")
    #         print(f"data : {data.user_id_} , {data.frd_id_}")
    #
    #         # 친구 요청
    #         if user_id == data.user_id_:
    #             send_id = data.frd_id_
    #
    #         # 요청 답변
    #         else:
    #             send_id = data.user_id_
    #
    #         print(send_id)
    #         for client in self.client.values():
    #             print(f"--- {client[1]}, {send_id}")
    #             if client[1] == send_id:
    #                 client[0].sendall(dumps(data))
    #                 break

    # 요청한 클라이언트에게만 전송
    # def send_client(self, sock: socket.socket, data):
    #     if self.connected():
    #         sock.sendall(pickle.dumps(data))
    #         return True
    #     else:
    #         return False

    # 접속한 모든 클라이언트에게 전송
    # def send_all_client(self, data):
    #     if self.connected():
    #         for client in self.client.values():
    #             client[0].sendall(pickle.dumps(data))
    #         return True
    #     else:
    #         return False
    #
    # # 같은 채팅방 멤버에게 발송
    # def send_message(self, data):
    #     if self.connected():
    #         if type(data) == ReqChat:
    #             member = self.db.find_user_chatroom(data.cr_id_)
    #         elif type(data) == JoinChat:
    #             member = data.member
    #
    #         print("sende message")
    #         print("member :", member)
    #
    #         for idx, client in enumerate(self.client.values()):
    #             print("-", client[1])
    #             if data.user_id_ != client[1] and client[1] in member:
    #                 client[0].sendall(pickle.dumps(data))
    #                 # self.db.insert_content(data)
    #
    #             # 메시지 발송내역은 한번만 저장
    #             if idx == 0:
    #                 self.db.insert_content(data)
    #         return True
    #     else:
    #         return False
    #
    # # 발송자를 제외한 나머지 접속자에게 발송
    # def send_exclude_sender(self, sock: socket.socket, data: LoginInfo):
    #     print("send_exclude_sender")
    #     if self.connected():
    #         for idx, client in enumerate(self.client.values()):
    #             if self.client[sock.getpeername()][1] != client[1]:
    #                 client[0].sendall(pickle.dumps(data))
    #         return True
    #     else:
    #         return False

    # 데이터 수신
    # def recevie(self, sock:socket.socket):
    #     # 데이터를 발송한 클라이언트의 어드레스 얻기
    #     try:
    #         receive_bytes = sock.recv(4096)
    #
    #         # 데이터 수신 실패시 오류 발생
    #         if not receive_bytes:
    #             raise
    #
    #         # 수신 받은 데이터 변환 하여 반환
    #         data = pickle.loads(receive_bytes)
    #         return data
    #
    #     except:
    #         self.disconnect(sock)
    #         sock.close()
    #         return None

    # 받은 데이터에 대한 처리 결과 반환 내용 넣기
    def process_data(self, sock, addr):
        print("before")
        print(f"data_type: {type(addr)}")
        print(f"data : {addr}")

        return sock, addr

    #     # 채팅 발송
    #     if type(data) == ReqChat:
    #         return data
    #
    #     # 아이디 중복 확인 요청
    #     elif type(data) == ReqDuplicateCheck:
    #         perdata: PerDuplicateCheck = self.db.membership_id_check(data)
    #
    #     # 인증메일 발송 요청
    #     elif type(data) == ReqEmailSend:
    #         perdata: PerEmailSend = self.db.email_check_1(data)
    #
    #     # 인증번호 확인 요청
    #     elif type(data) == ReqEmailNumber:
    #         perdata: PerEmailNumber = self.db.email_check_2(data)
    #
    #     # 회원가입 요청
    #     elif type(data) == ReqMembership:
    #         perdata: PerRegist = self.db.regist(data)
    #         # self.db.insert_content(ReqChat("PA_1", "", f"'{data.user_id_}'님이 입장했습니다."))
    #
    #     # 로그인 요청
    #     elif type(data) == ReqLogin:
    #         perdata: PerLogin = self.db.login(data)
    #         if perdata.rescode == 2:
    #             self.client[sock.getpeername()][1] = perdata.user_id_
    #             perdata.login_info = self.get_login_list()
    #
    #     # 로그 아웃
    #     elif type(data) == ReqLoout:
    #         user_id = self.client[sock.getpeername()][1]
    #         self.client[sock.getpeername()][1] = ""
    #         perdata: LoginInfo([user_id], False)
    #
    #     # 유저 프로필 사진, 상태메세지 변경
    #     elif type(data) == ReqStateChange:
    #         perdata: ReqStateChange = self.db.change_user_state(data)
    #
    #     elif type(data) == JoinChat:
    #         self.db.create_chatroom(data)
    #         self.db.insert_content(ReqChat("", "", ", ".join(data.member)+"님이 입장했습니다."))
    #         perdata = data
    #
    #     # 친구 요청 보내기
    #     elif type(data) == ReqSuggetsFriend:
    #         self.db.insert_friend(data)
    #         perdata: ReqSuggetsFriend(data.user_id_, data.frd_id_)
    #
    #     # 친구 응답 보내기
    #     elif type(data) == PerAcceptFriend:
    #         if data.result == 1:
    #             self.db.update_friend(data)
    #             perdata: PerAcceptFriend(data.user_id_, data.frd_id_, 1)
    #         # 거절
    #         else:
    #             self.db.delete_friend(data)
    #             perdata: PerAcceptFriend(data.user_id_, data.frd_id_, 0)
    #
    #     # 유저 나가기 요청
    #     elif type(data) == DeleteTable:
    #         self.db.delete_table(data)
    #         self.db.insert_content(ReqChat("", "", ", ".join(data.my_name) + "님이 입장했습니다."))
    #         perdata = data
    #     else:
    #         return data
    #
    #     print("after")
    #     print(f"process_data : {type(perdata)}")
    #     print("perdata", get_data_tuple(data))
    #     print()
    #     return perdata

    # def get_login_list(self):
    #     login_list = list()
    #     for client in self.client.values():
    #         if client[1] != "":
    #             login_list.append(client[1])
    #
    #     print("login info")
    #     print(login_list)
    #
    #     return login_list

    # def db_log_inout_state_save(self, rescode):
    #     """로그인 / 로그아웃 내역(시간) USER_LOG에 저장"""
    #     time_ = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    #     print(time_)
    #     print(rescode)
    #     if rescode == 2:
    #         sql_ = f"UPDATE TB_LOG SET LOGIN_TIME = '{time_}' WHERE USER_ID = '{id}'"
    #         self.db.conn.execute(sql_)
    #         self.db.conn.commit()
    #     All_TB_LOG = self.db.conn.execute("SELECT * FROM TB_LOG").fetchall()
    #     if not All_TB_LOG:
    #         print("예외처리 : TB_LOG에 아무것도 없습니다.")

#     def handler(self, sock, addr):
#         while True:
#             data = self.recevie(sock)
#
#             if not data:
#                 break
#
#             print("[ 데이터 수신중 ]")
#             # 수신된 데이터에 따른 결과 반환값을 클라이언트로 보내주기
#             print(data)
#
#             while True:
#                 try:
#                     process_data = self.process_data(sock, addr)
#                     print("[ 데이터 처리중 ]")
#                     self.send(sock, process_data)
#                     print("[ 데이터 처리완 ]")
# `                except Exception as e:
#                     # 오류 확인
#                     print(f"Error occurred: {e}")`
#
# if __name__ == "__main__":
#     server = Server()
#
#     while True:
#         print("서버 ON AND Watiting..")
#
#         c_sock, c_addr = server.accept()
#         c_thread = Thread(target=server.handler, args=(c_sock, c_addr), daemon=True)
#         c_thread.start()
