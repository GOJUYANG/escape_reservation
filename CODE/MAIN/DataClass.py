import pandas

# --- 사용자 요청
# 사용자의 채팅 전송 요청
class ReqUserChat:
    def __init__(self, user_id: str, msg_type: str, user_nm: str, msg: str, send_time: str):
        self.user_id = user_id
        self.msg_type = msg_type
        self.msg = msg
        self.send_time = send_time

# 아이디 중복확인 검사요청
class ReqDuplicateCheck:
    def __init__(self, id_:str):
        self.id_ = id_

# 유효 이메일 확인
class ReqValidEmail:
    def __init__(self, email_addr: str):
        self.email_addr = email_addr

# 사용자 회원가입 요청
class ReqJoin:
    def __init__(self, id_: str, pw: str, nm: str, email: str, c_date: str, img: str):
        self.id_ = id_
        self.pw = pw
        self.nm = nm
        self.email = email
        self.c_date = c_date
        self.img = img

# 사용자의 구독알림 요청
class ReqSubTheme:
    def __init__(self, user_id:str, req_date: str, th_nm: str, th_time: str):
        self.user_id = user_id
        self.req_date = req_date
        self.th_nm = th_nm
        self.th_time = th_time

# 사용자의 예약확인 요청
class ReqResUserOK:
    def __init__(self, user_id:str, user_addr:str, req_date: str, th_nm: str, th_date: str, th_time: str, th_price: str,
                 th_num: str, th_name: str, th_phone: str, th_paytype: str):
        self.user_id = user_id
        self.user_addr = user_addr
        self.req_date = req_date
        self.th_nm = th_nm
        self.th_date = th_date
        self.th_time = th_time
        self.th_price = th_price
        self.th_num = th_num
        self.th_name = th_name
        self.th_phone = th_phone
        self.th_paytype = th_paytype

# --- 관리자 요청
# 관리자의 채팅 전송 요청
class ReqMngChat:
    def __init__(self, manager_id: str, msg: str):
        self.manager_id = manager_id
        self.msg = msg

# 관리자의 채팅방 리스트 요청
class CallAllChat:
    def __init__(self, res_no:int, res_id, res_ip, last_date, last_nm):
        self.res_no = res_no
        self.res_id = res_id
        self.res_ip = res_ip
        self.last_date = last_date
        self.last_nm = last_nm

# 관리자의 예약 / 구독 승인 요청 + 이메일 전송
class ResMngOk:
    def __init__(self, r_email: str, e_type: str):
        self.r_email = r_email
        self.e_type = e_type

# 관리자의 예약수정 요청
class ReqResFix:
    def __init__(self, th_nm: str, th_date: str, th_time: str, th_price: str,
                 th_num: str, th_name: str, th_phone: str, th_paytype: str):
        self.th_nm = th_nm
        self.th_date = th_date
        self.th_time = th_time
        self.th_price = th_price
        self.th_num = th_num
        self.th_name = th_name
        self.th_phone = th_phone
        self.th_paytype = th_paytype

# 관리자의 예약취소 요청
class ReqResCancel:
    def __init__(self, th_nm: str, th_date: str, th_time: str, th_price: str,
                 th_num: str, th_name: str, th_phone: str, th_paytype: str):
        self.th_nm = th_nm
        self.th_date = th_date
        self.th_time = th_time
        self.th_price = th_price
        self.th_num = th_num
        self.th_name = th_name
        self.th_phone = th_phone
        self.th_paytype = th_paytype

# --- 공통 요청

# 로그인 요청
class ReqLogin:
    def __init__(self, login_id: str, login_pw: str):
        self.login_id = login_id
        self.login_pw = login_pw

# 사용자, 관리자의 채팅 조회 요청
class ChatCNT:
    def __init__(self, user_id:str):
        self.user_id = user_id

# 사용자, 관리자의 로그아웃 요청
class Logout:
    def __init__(self, user_id: str):
        self.user_id = user_id

# 사용자, 관리자의 채팅 삭제 요청
class DeleteChat:
    def __init__(self, user_id: str):
        self.user_id = user_id

# --- 서버의 허가응답

# 채팅 송수신 응답
class Perchat:
    def __init__(self, sender_id: str, msg: str):
        self.sender_id = sender_id
        self.msg = msg

# 로그인 허가 응답 : 허가번호, 아이디
# rescode = 0 ("아이디 존재하지 않음")
# rescode = 1 ("비밀번호 존재하지 않음")
# rescode = 2 ("로그인 허가 완료")
class PerLogin:
    def __init__(self, rescode: int, login_id: str, user_info: list):
        self.rescode = rescode
        self.login_id = login_id
        self.user_info = user_info

# 로그인 유저 정보 발송
# len(list)=1: 신규로 로그인/로그아웃 발행할때 발송용
# len(list)>1: 전체 로그인 유저 정보 발송용
class LoginInfo:
    def __init__(self, id_: list, login=True):
        self.id_ = id_
        self.login = login

# 아이디 중복 체크 응답 : True(중복), False(중복아님)
class PerDuplicateCheck:
    def __init__(self, isExisited: bool):
        self.isExisited = isExisited

#유효이메일 응답
class PerValidEmail:
    def __init__(self, isValid: bool):
        self.isValid = isValid

# 회원가입 허가 응답
class PerJoin:
    def __init__(self, Success: bool):
        self.Success = Success

# 예약 승인요청 허가응답(데이터 저장)
class PerResOk:
    def __init__(self, savedone: bool):
        self.savedone = savedone

# 예약수정 허가 응답
class PerResfix:
    def __init__(self, isfix: bool):
        self.isfix = isfix

# 예약취소 허가 응답
class PerResCancel:
    def __init__(self, iscancel: bool):
        self.iscancel = iscancel

# 사용자 구독요청 허가응답(데이터저장)
class PerSubTheme:
    def __init__(self, isSaved: bool):
        self.isSaved = isSaved

# 이메일 전송 허가 응답
class PerEmailSend:
    def __init__(self,send_type:str):
        self.send_type = send_type
