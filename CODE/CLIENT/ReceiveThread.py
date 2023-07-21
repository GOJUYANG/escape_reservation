from PyQt5.QtCore import QThread, pyqtSignal

from CODE.CLIENT import Client
from CODE.MAIN.DataClass import *

class ReceiveThread(QThread):

    # 시그널 선언
    res_user_message = pyqtSignal(ReqUserChat)
    res_manager_message = pyqtSignal(ReqMngChat)

    res_duplicate_id_check = pyqtSignal(PerDuplicateCheck)
    res_emailcheck = pyqtSignal(PerValidEmail)
    res_join = pyqtSignal(PerJoin)

    res_login = pyqtSignal(PerLogin)
    res_delete_chat = pyqtSignal(DeleteChat)

    res_ok = pyqtSignal(PerResOk)
    res_subscribe = pyqtSignal(PerSubTheme)

    res_fix = pyqtSignal(PerResfix)
    res_cancel = pyqtSignal(PerResCancel)
    res_email = pyqtSignal(PerEmailSend)

    def __init__(self, client:Client):
        super().__init__()
        self.client = client

    def run(self) -> None:
        while True:
            data = self.client.recevie()

            print("[ 데이터 수신 ]")
            print(f"수신 데이터 타입 : {type(data)}")

            # 수신된 데이터 타입에 따른 시그널 방향 제시 : 클라이언트가 받을 결과를 전송하는 것임

            # 채팅 수신
            if type(data) == ReqUserChat:
                self.res_user_message.emit(data)

            elif type(data) == ReqMngChat:
                self.res_manager_message.emit(data)

            # 아이디 중복 확인
            elif type(data) == PerDuplicateCheck:
                self.res_duplicate_id_check.emit(data)

            elif type(data) == PerValidEmail:
                self.res_emailcheck.emit(data)

            # 회원가입 요청 결과
            elif type(data) == PerJoin:
                self.res_join.emit(data)

            # 로그인 결과
            elif type(data) == PerLogin:
                self.res_login.emit(data)

            # 서버 대화테이블 삭제
            elif type(data) == DeleteChat:
                self.res_delete_chat.emit(data)

            # 예약승인
            elif type(data) == PerResOk:
                self.res_ok.emit(data)

            # 구독요청
            elif type(data) == PerSubTheme:
                self.res_subscribe.emit(data)

            # 예약 수정
            elif type(data) == PerResfix:
                self.res_fix.emit(data)

            # 예약취소
            elif type(data) == PerResCancel:
                self.res_cancel.emit(data)

            # 예약내역발송
            elif type(data) == PerEmailSend:
                self.res_email.emit(data)
