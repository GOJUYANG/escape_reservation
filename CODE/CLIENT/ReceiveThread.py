# from PyQt5.QtCore import QThread, pyqtSignal
#
# from Source.Client import Client
# from Source.Main.DataClass import *
#
# class ReceiveThread(QThread):
#
#     # 시그널 선언
#     res_message = pyqtSignal(ReqChat)
#     res_duplicate_id_check = pyqtSignal(PerDuplicateCheck)
#     res_emailcheck_1 = pyqtSignal(PerEmailSend)
#     res_emailcheck_2 = pyqtSignal(PerEmailNumber)
#     res_regist = pyqtSignal(PerRegist)
#     res_login = pyqtSignal(PerLogin)
#     res_change_state = pyqtSignal(ReqStateChange)
#
#     res_delete_table = pyqtSignal(DeleteTable)
#
#     login_info_updata = pyqtSignal(LoginInfo)
#     join_chat = pyqtSignal(JoinChat)
#
#     req_friend = pyqtSignal(ReqSuggetsFriend)
#     per_friend = pyqtSignal(PerAcceptFriend)
#
#     def __init__(self, client:Client):
#         super().__init__()
#         self.client = client
#
#     def run(self) -> None:
#         while True:
#             data = self.client.recevie()
#
#             print("[ 데이터 수신 ]")
#             print(f"수신 데이터 타입 : {type(data)}")
#
#             # 수신된 데이터 타입에 따른 시그널 방향 제시 : 클라이언트가 받을 결과를 전송하는 것임
#
#             # 채팅 수신
#             if type(data) == ReqChat:
#                 self.res_message.emit(data)
#
#             # 아이디 중복 확인
#             elif type(data) == PerDuplicateCheck:
#                 self.res_duplicate_id_check.emit(data)
#
#             # 인증번호 발송
#             elif type(data) == PerEmailSend:
#                 self.res_emailcheck_1.emit(data)
#
#             # 인증번호 확인
#             elif type(data) == PerEmailNumber:
#                 self.res_emailcheck_2.emit(data)
#
#             # 회원가입 요청 결과
#             elif type(data) == PerRegist:
#                 self.res_regist.emit(data)
#
#             # 로그인 결과
#             elif type(data) == PerLogin:
#                 self.res_login.emit(data)
#
#             # 유저 프로필, 상태메시지 변경
#             elif type(data) == ReqStateChange:
#                 self.res_change_state.emit(data)
#
#             # 서버 대화테이블 삭제
#             elif type(data) == DeleteTable:
#                 self.res_delete_table.emit(data)
#
#             # 로그인시 유저 관련 정보 받기
#             elif type(data) == LoginInfo:
#                 self.login_info_updata.emit(data)
#
#             # 채팅방 개설
#             elif type(data) == JoinChat:
#                 self.join_chat.emit(data)
#
#             elif type(data) == ReqSuggetsFriend:
#                 self.req_friend.emit(data)
#
#             elif type(data) == PerAcceptFriend:
#                 self.per_friend.emit(data)
