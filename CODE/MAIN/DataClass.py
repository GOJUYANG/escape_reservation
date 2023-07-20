from datetime import datetime


# 클래스 이름 시작 단어 기준으로 구분
# Req : 클라이언트 → 서버
# Per : 서버 → 클라이언트

# 참여 채팅방 정보를 불러와서 대화에 참여하고 있는 개인 채팅방 목록을 불러온다.
# 채팅방 번호(타입), 채팅방 멤버
class CallSchatList:
    def __init__(self, chat_room_id: str, chat_room_members: list):
        self.chat_room = chat_room_id
        self.chat_room_members = chat_room_members

# 참여 채팅방 정보를 불러와서 대화에 참여하고 있는 단체 채팅방 목록을 불러온다.
# 채팅방 번호(타입), 채팅방 멤버
class CallGchatList:
    def __init__(self, chat_room_id: str, chat_room_members: list):
        self.chat_room = chat_room_id
        self.chat_room_members = chat_room_members

# 참가자가 입장할 때 채팅방에 접속인원을 알려준다.
# 참여멤버
class ReqJoinMember:
    def __init__(self, my_id: str, members: list):
        self.my_id = my_id
        self.members = members

# 채팅 송신 허가 응답
# 발신 아이디, 메세지
class PerChat:
    def __init__(self, sender_id: str, msg: str):
        self.sender_id = sender_id
        self.msg = msg

# 유저가 입력한 메세지가 아이디, 번호, 내용, 시간이 db에 저장된다.
# 아이디, 번호, 내용, 시간
class ReqSaveChat:
    def __init__(self, id: str, msg: str, time: str):
        self.id = id
        self.msg = msg
        self.time = time

# 친구요청을 하면 요청자와 친구 아이디를 넘겨준다.
# (요청자 아이디, 수락자 아이디), 허락여부
class PlusFriend:
    def __init__(self, id_tuple: tuple, result: bool):
        self.id_tuple = id_tuple
        self.result = result

# 로그아웃을 하면 접속상태를 0으로 변경시킨다.
class ReqLogout:
    def __init__(self, id: str):
        self.id = id

# 사용자의 프로필과 상태메세지를 변경할 수 있다.
# 유저아이디, 상태메세지
class ReqStateChange:
    def __init__(self, user_id: str, user_state: str, user_img:str):
        self.user_id = user_id
        self.user_state = user_state
        self.user_img = user_img

# 사용자의 채팅창 배경이미지를 변경할 수 있다.
# 유저아이디, 채팅창 배경이미지 경로
# class ReqImgChange:
#     def __init__(self, user_id: str, user_chatimg_path: str):
#         self.user_id = user_id
#         self.user_chatimg_path = user_chatimg_path

# 친구 리스트가 우측에 출력된다.
# 사용자 프로필, 친구 이름, 접속 상태
class ShowFrdList:
    def __init__(self, user_profile: str, friend_name: str, is_online: bool):
        self.user_profile: user_profile
        self.friend_name = friend_name
        self.is_online = is_online

# 나가기를 누른 CTB_CHATROOM 테이블에서 CR_ID에 맞는 행들만 삭제한다.
# 내 아이디, 나간 채팅방 아이디
class DeleteMyTable:
    def __init__(self, my_id: str, cr_id: str):
        self.my_id = my_id
        self.cr_id = cr_id

# 1. 해당 CR_ID의 TB_CONTENT, TB_READ_CNT 테이블을 삭제한다.
# 2. TB_CHATROOM에서 CR_ID 삭제
# 참여멤버가 0인 채팅방 아이디
class DeleteTable:
    def __init__(self, cr_id: str, my_id: str, my_name:str):
        self.cr_id = cr_id
        self.my_id = my_id
        self.my_name = my_name

# ==================== 로그인

# 로그인 요청 : 아이디, 비밀번호
class ReqLogin:
    def __init__(self, id_:str, pw:str):
        self.id_ = id_
        self.password = pw

# 로그인 허가 응답 : 허가번호, 아이디
# rescode = 0 ("아이디 존재하지 않음")
# rescode = 1 ("비밀번호 존재하지 않음")
# rescode = 2 ("로그인 허가 완료")
class PerLogin:
    def __init__(self, rescode: int, user_id_:str, login_info=[], user_info=[]):
        self.rescode = rescode
        self.user_id_ = user_id_
        self.login_info = login_info
        self.user_info = user_info

# 로그인 유저 정보 발송
# len(list)=1: 신규로 로그인/로그아웃 발행할때 발송용
# len(list)>1: 전체 로그인 유저 정보 발송용
class LoginInfo:
    def __init__(self, id_: list, login=True):
        self.id_ = id_
        self.login = login

# ==================== 로그아웃

# 로그아웃 요청 : 아이디, 시간
class ReqLoout:
    def __init__(self, id_: str):
        self.id_ = id_


# ==================== 회원가입

# 회원가입 중복 아이디 체크 요청 : 아이디
class ReqDuplicateCheck:
    def __init__(self, id_:str):
        self.id_ = id_

# 아이디 중복 체크 응답 : True(중복), False(중복아님)
class PerDuplicateCheck:
    def __init__(self, isExisited: bool):
        self.isExisited = isExisited

# 회원가입 요청 : 아이디, 비밀번호, 닉네임, 이메일, 가입일자, 프로필 이미지경로, 상태메세지
class ReqMembership:
    def __init__(self, id_: str, pw: str, nm: str, email: str, c_date: str, img: str):
        self.id_ = id_
        self.pw = pw
        self.nm = nm
        self.email = email
        self.c_date = c_date
        self.img = img

# 회원가입 허가 응답
class PerRegist:
    def __init__(self, Success: bool):
        self.Success = Success

# 이메일 유효성 확인 및 전송 요청
class ReqEmailSend:
    def __init__(self, r_email: str):
        self.r_email = r_email

# 이메일 전송 응답
class PerEmailSend:
    def __init__(self, isSend: bool):
        self.isSend = isSend

# 이메일 인증번호 확인 요청
class ReqEmailNumber:
    def __init__(self, num1: str, num2: str):
        self.num1 = num1
        self.num2 = num2

# 이메일 인증번호 일치 여부 응답
class PerEmailNumber:
    def __init__(self, ismatch: bool):
        self.ismatch = ismatch

# ==================== 친구 초대

# 친구 초대 요청
class ReqSuggetsFriend:
    def __init__(self, user_id_: str, frd_id_: str, result=0):
        self.user_id_ = user_id_
        self.frd_id_ = frd_id_
        self.result = result

# 친구 수락 허가 응답
class PerAcceptFriend:
    def __init__(self, user_id_: str, frd_id_: str, result=0):
        self.user_id_ = user_id_
        self.frd_id_ = frd_id_
        self.result = result

# ==================== 채팅방 개설

# 채팅방 요청
class JoinChat:
    def __init__(self, user_id_: str, member_id: list, member_name: list, title:str, cr_id_=""):
        self.user_id_ = user_id_
        self.member_id = member_id
        self.member_name = member_name
        self.title = title
        self.cr_id_ = cr_id_

# 채팅방 나가기
class OutChat:
    def __init__(self, cr_id_: str, user_id_: str):
        self.cr_id_ = cr_id_
        self.user_id_ = user_id_

def get_data_tuple(t_class):
    data_dict = t_class.__dict__
    data_tuple = tuple(data_dict.values())
    return data_tuple

# ==================== 메시지 송신

# 채팅 송수신
class ReqChat:
    def __init__(self, cr_id_:str, user_id_:str, msg: str, user_nm=""): #msg = self.edt_txt.text()
        self.cr_id_ = cr_id_
        self.user_nm = user_nm
        self.user_id_ = user_id_
        self.msg = msg

class ReadChat:
    def __init__(self, cr_id_:str):
        self.cr_id_ = cr_id_
        self.msg:pandas.DataFrame