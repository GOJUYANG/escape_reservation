import random
import datetime
import folium
import re

# 이메일 전송을 위한 SMTP프로토콜 접근 지원을 위한 라이브러리
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QMainWindow, QApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QUrl, Qt
from PyQt5 import QtWebEngineWidgets

from CODE.SCREEN.UI_MainWidget import Ui_MainWindow
# from CODE.SCREEN.ChatBox import ChatBox
from CODE.SCREEN.DialongWarning import DialogWarning

from CODE.SERVER.DataRead import DataRead
from CODE.MAIN.DataClass import *

from CODE.CLIENT.Client import Client
from CODE.CLIENT.ReceiveThread import ReceiveThread

class Theme():
    def __init__(self, gridlayout, num, list_NM, list_IMG):
        self.num = num
        self.list_NM = list_NM
        self.list_IMG = list_IMG
        self.gridlayout = gridlayout


    def create_theme(self):
        for i in range(0, self.num, 4):
            theme_container = QWidget()
            theme_container.setFixedSize(680, 231)
            layout = QHBoxLayout(theme_container)

            for j in range(4):
                idx = i + j
                if idx < self.num:
                    lb_img = QLabel()
                    lb_img.setPixmap(QPixmap(self.list_IMG[idx]))
                    lb_img.setScaledContents(True)

                    lb_nm = QLabel()
                    lb_nm.setAlignment(Qt.AlignCenter)
                    lb_nm.setText(self.list_NM[idx])

                    # 이미지와 사진 수직배치
                    vbox = QVBoxLayout()
                    vbox.addWidget(lb_img)
                    vbox.addWidget(lb_nm)

                    # 컨테이터에 수직 레이아웃 추가
                    layout.addLayout(vbox)

            theme_container.setLayout(layout)
            self.gridlayout.addWidget(theme_container, i, 0, 1, 1)
        layout = QVBoxLayout(theme_container)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 변수 초기화
        self.res_available = True
        self.mouse_x: int = 0
        self.mouse_y: int = 0

        self.r_email = ''
        self.user_id = ""
        self.use_id = False

        # --- 인증메일 송신자
        self.s_email = 'rhrnaka@gmail.com'
        self.s_pwd = 'sxrrxnbbfstqniee'

        # ---클래스 호출
        self.dlg_warning = DialogWarning()

        # --- DB연결
        self.db = DataRead()
        self.theme_df = self.db.return_df('*', 'THEME_INFO')
        print(self.theme_df.memory_usage(deep=True).sum())

        # --- 서버 연결
        self.client = Client()
        if not self.client.connect():
            self.dlg_warning.set_dialog_type(1, 'cannot_service')
            self.dlg_warning.exec()
            exit()
        else:
            self.receive_thread = ReceiveThread(self.client)
            self.address = self.client.address()
            self.connect_thread_signal()
            self.receive_thread.start()

        # --- qwebview 객체 생성
        self.webview = QtWebEngineWidgets.QWebEngineView(self.widget_map)
        self.webview.resize(591, 411)

        # --- 함수 호출
        self.init_ui()
        self.connect_event()
        self.widget_clicked()
        self.inset_folium()
        self.insert_theme()
        self.label_clicked()
        self.insert_single_theme(0)

    def init_ui(self):
        from PyQt5.QtCore import Qt
        self.setWindowFlags(Qt.FramelessWindowHint)

    def closeEvent(self, a0):
        self.db.end_conn()
        self.client.disconnect()
        self.thread().disconnect()
        self.close()

    def shut_down(self):
        self.close()

    def connect_event(self):
        # ---버튼 연결
        #===로그인===#
        self.btn_login_exit.clicked.connect(self.shut_down)
        self.btn_join_login.clicked.connect(self.check_login_info)
        self.lb_login_pwd.returnPressed.connect(self.check_login_info)
        self.btn_membership.clicked.connect(lambda _, index=1: self.move_page(index))
        self.btn_join_cancel.clicked.connect(lambda _, index=0: self.move_page(index))

        # ===회원가입===#
        self.btn_check_id.clicked.connect(self.check_duple_id)
        self.btn_check_email.clicked.connect(self.check_valid_email)
        self.btn_join_ship.clicked.connect(self.check_membership_info)
        self.btn_join_cancel.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_login))

    def connect_thread_signal(self):
        # ===로그인===#
        self.receive_thread.res_login.connect(self.check_login)

        # ===회원가입===#
        self.receive_thread.res_join.connect(self.result_join)
        self.receive_thread.res_duplicate_id_check.connect(self.check_id)
        self.receive_thread.res_emailcheck.connect(self.check_email_condition)

    def move_page(self, index):
        """stackedwidget 페이지 이동"""
        self.Manager_stack.setCurrentIndex(index)

    def check_login_info(self):
        login_id = self.lb_login_id.text()
        login_pw = self.lb_login_pw.text()
        print(login_id, login_pw)

        self.client.send(ReqLogin(login_id, login_pw))

    def check_login(self, data: PerLogin):
        """qt : 입력 ID, PASSWORD 확인 함수"""
        if data.rescode == 0:
            self.dlg_warning.set_dialog_type(1, 'login', "※로그인 실패※ \n 존재하지 않는 아이디/비밀번호 입니다. \n 다시 확인해주세요.")
            self.dlg_warning.exec()
            return False
        elif data.rescode == 1:
            self.dlg_warning.set_dialog_type(1, 'login', "※로그인 실패※ \n 잘못된 아이디 또는 패스워드 입니다.")
            self.dlg_warning.exec()
            return False
        else:
            self.dlg_warning.set_dialog_type(1, 'login', f"※로그인 완료※ \n {data.login_id}님 로그인 완료")
            self.dlg_warning.exec()

    def check_id_condition(self):
        """아이디 5~16자 조건 확인"""
        if 5 <= len(self.lb_ship_id.text()) <= 16:
            return True
        else:
            return False

    def check_pwd_condition(self):
        """비밀번호 조건 확인 함수 : 영대문자(1), 특수문자(1) 필수포함 및 최대 16자"""

        insert_pwd = self.lb_ship_pwd1.text()

        # 영대문자
        upper_mathct = re.match('.*[A-Z]+.*', insert_pwd)
        # 특수문자
        special_mark = re.findall('[`~!@#$%^&*(),<.>/?]+', insert_pwd)

        check = True
        if not upper_mathct:
            txt = "pw_alphabet_1"
            check = False
        elif not special_mark:
            txt = "pw_unique_word"
            check = False
        elif len(insert_pwd) < 5 or len(insert_pwd) > 16:
            check = False
            txt = "pw_len_limited"

        if not check:
            return check, txt

        all_condition = '^(?=.*[A-Z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{5,16}$'
        if re.match(all_condition, insert_pwd):
            return True, ''

    def check_between_pwd(self):
        """비밀번호1, 2 일치 확인"""
        insert_pwd_1 = self.lb_ship_pwd1.text()
        insert_pwd_2 = self.lb_ship_pwd2.text()

        if insert_pwd_1 == '':
            txt = "pw_input"
        elif insert_pwd_2 == '':
            txt = "pw_input"

        if insert_pwd_1 != insert_pwd_2:
            txt = "pw_not_match"
            return False, txt
        else:
            return True, ''

    def check_nickname_condition(self):
        """닉네임 최대 20자 조건 확인 : 20자 이하의 한글/영문/숫자 조합"""
        insert_nickname = self.lb_ship_name.text()

        if len(insert_nickname) > 20:
            txt = "nick_name_len_limit"
            return False, txt
        elif len(insert_nickname) == 0:
            txt = "nick_name_no_input"
            return False, txt
        else:
            return True, ''

    #클라이언트 이메일 유효확인
    def check_valid_email(self):
        if len(self.lb_ship_email.text()) == 0:
            self.dlg_warning.set_dialog_type(1, 'email_no_input')
            self.dlg_warning.exec()
        else:
            email = self.lb_ship_email.text() + self.cmb_ship_email.currentText()
            self.client.send(ReqValidEmail(email))

    def check_email_condition(self, data:PerValidEmail):
        if data.isValid:
            self.dlg_warning.set_dialog_type(1, 'vaild_email')
        else:
            self.dlg_warning.set_dialog_type(1, 'not_vaild_email_addr')
        self.dlg_warning.exec()

    def check_membership_info(self):
        """send: 회원가입 입력 정보"""
        id_ = self.lb_ship_id.text()
        pwd = self.lb_ship_pwd1.text()
        nm = self.lb_ship_name.text()
        email = self.lb_ship_email.text()
        email_addr = self.cmb_ship_email.currentText()
        c_date = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        img = f'../../IMG/profile/{random.randint(1,5)}.png'

        # 아이디 확인
        if not self.check_id_condition():
            self.dlg_warning.set_dialog_type(1, 'id_len_limited')
            self.dlg_warning.exec()

        # 비밀번호 확인
        elif not self.check_pwd_condition()[0]:
            self.dlg_warning.set_dialog_type(1, self.check_pwd_condition()[1])
            self.dlg_warning.exec()

        # 비밀번호+비밀번호확인 확인
        elif not self.check_between_pwd()[0]:
            self.dlg_warning.set_dialog_type(1, self.check_between_pwd()[1])
            self.dlg_warning.exec()

        # 닉네임 확인
        elif not self.check_nickname_condition()[0]:
            self.dlg_warning.set_dialog_type(1, self.check_nickname_condition()[1])
            self.dlg_warning.exec()

        # 아이디 중복확인 진행 여부
        elif not self.use_id:
            self.dlg_warning.set_dialog_type(1, "used_id_no_check")
            self.dlg_warning.exec()

        else:
            self.user_id = id_
            self.client.send(ReqJoin(id_, pwd, nm, email+email_addr, c_date, img))
            self.move_page(0)

    def result_join(self, data: PerJoin):
        if data.Success:
            self.dlg_warning.set_dialog_type(2, "success_join_membership")
            if self.dlg_warning.exec():
                self.move_main_widget()
        else:
            self.dlg_warning.set_dialog_type(2, "failed_join_membership")
            self.dlg_warning.exec()

    def check_duple_id(self):
        check_id = self.lb_ship_id.text()
        self.client.send(ReqDuplicateCheck(check_id))

    def check_id(self, data: PerDuplicateCheck):
        if data.isExisited:
            self.dlg_warning.set_dialog_type(1, 'used_id')
        else:
            self.dlg_warning.set_dialog_type(1, 'user_can_use_id')
            self.use_id = True
        self.dlg_warning.exec()

    def mousePressEvent(self, e):
        cur_idx = self.Client_stack.currentIndex()
        if cur_idx == 0:
            mouse_x, mouse_y = e.x(), e.y()
            print(f"{mouse_x}, {mouse_y}")
            self.move_detail_page(mouse_x, mouse_y)

    def move_detail_page(self, x, y):
        if 184 <= x <= 335 and 55 <= y <= 241:
            self.Client_stack.setCurrentIndex(1)
            self.insert_single_theme(0)
        elif 352 <= x <= 505 and 51 <= y <= 239:
            self.Client_stack.setCurrentIndex(1)
            self.insert_single_theme(1)
        elif 520 <= x <= 661 and 57 <= y <= 232:
            self.Client_stack.setCurrentIndex(1)
            self.insert_single_theme(2)
        elif 690 <= x <= 830 and 58 <= y <= 234:
            self.Client_stack.setCurrentIndex(1)
            self.insert_single_theme(3)
        elif 186 <= x <= 323 and 285 <= y <= 461:
            self.Client_stack.setCurrentIndex(1)
            self.insert_single_theme(4)
        elif 358 <= x <= 497 and 292 <= y <= 468:
            self.Client_stack.setCurrentIndex(1)
            self.insert_single_theme(5)
        elif 522 <= x <= 659 and 290 <= y <= 458:
            self.Client_stack.setCurrentIndex(1)
            self.insert_single_theme(6)
        elif 689 <= x <= 835 and 292 <= y <= 468:
            self.Client_stack.setCurrentIndex(1)
            self.insert_single_theme(7)
        elif 198 <= x <= 376 and 520 <= y <= 616:
            self.Client_stack.setCurrentIndex(1)
            self.insert_single_theme(8)
        elif 408 <= x <= 602 and 438 <= y <= 617:
            self.Client_stack.setCurrentIndex(1)
            self.insert_single_theme(9)
        elif 630 <= x <= 834 and 442 <= y <= 614:
            self.Client_stack.setCurrentIndex(1)
            self.insert_single_theme(10)

    def widget_clicked(self):
        self.widget_theme.mousePressEvent = lambda e, name='theme': self.mousePressEvent(e, name)
        self.widget_reservation.mousePressEvent = lambda e, name='reservation': self.mousePressEvent(e, name)
        self.widget_folium.mousePressEvent = lambda e, name='folium': self.mousePressEvent(e, name)
        self.widget_request.mousePressEvent = lambda e, name='request': self.mousePressEvent(e, name)

    def label_clicked(self):
        list_NM = self.theme_df.TH_NM.tolist()
        lb_th_list = []
        for i in range(len(list_NM)):
            lb_th_list.append(getattr(self, f"th_{i + 1}"))
            lb_th_list[i].mousePressEvent = lambda x=None, y=i: self.insert_single_theme(y)

    def move_stack(self, e, name):
        list_frame = [self.frame_theme, self.frame_reservation, self.frame_folium, self.frame_request]
        if name == 'theme':
            self.Client_stack.setCurrentIndex(0)
            list_frame[0].show()
            list_frame[1].hide()
            list_frame[2].hide()
            list_frame[3].hide()
        elif name == 'reservation':
            self.Client_stack.setCurrentIndex(1)
            self.insert_single_theme(0)
            list_frame[0].hide()
            list_frame[1].show()
            list_frame[2].hide()
            list_frame[3].hide()
        elif name == 'folium':
            self.Client_stack.setCurrentIndex(4)
            list_frame[0].hide()
            list_frame[1].hide()
            list_frame[2].show()
            list_frame[3].hide()
        elif name == 'request':
            self.Client_stack.setCurrentIndex(5)
            list_frame[0].hide()
            list_frame[1].hide()
            list_frame[2].hide()
            list_frame[3].show()

    def insert_theme(self):
        theme_df = self.db.return_df('*', 'THEME_INFO')
        print(theme_df)
        list_NM = theme_df.TH_NM.tolist()
        list_IMG = theme_df.TH_IMG.tolist()
        num = len(list_NM)
        theme = Theme(self.gridLayout_2, num, list_NM, list_IMG)
        theme.create_theme()

    def insert_single_theme(self, idx: int):
        """테마 버튼 클릭 시 테마 하나에 대한 정보 출력"""

        list_NM = self.theme_df.TH_NM.tolist()
        list_IMG = self.theme_df.TH_IMG.tolist()
        list_content = self.theme_df.TH_CONTENT.tolist()
        list_lv = self.theme_df.TH_LV.tolist()

        num_df = self.theme_df.TH_NUM.iloc[idx]
        num_list = num_df.split(',')

        restime_df = self.theme_df.TH_RESTIME.iloc[idx]
        restime_list = restime_df.split(',')

        list_lb_th = []
        list_btn_time = []
        for i in range(len(list_NM)):
            list_lb_th.append(getattr(self, f"th_{i + 1}"))
            list_lb_th[i].setText(list_NM[i])

        # 예약시간 버튼
        for j in range(len(restime_list)):
            list_btn_time.append(getattr(self, f"btn_time_{j + 1}"))
            if self.res_available:
                available = '예약가능'
                list_btn_time[j].setText(f"{restime_list[j]}" + '\n' + f"{available}")

        # 탭 클릭시 초기 화면 설정
        self.lb_th_img.setPixmap(QPixmap(list_IMG[idx]))
        self.lb_theme_title.setText(list_NM[idx])
        self.lb_th_info.setText(list_content[idx])

        lv = int(list_lv[i])
        star = '★★★★★'
        self.lb_theme_lv.setText(star[:lv] + star[-(5 - lv):].replace('★', '☆'))
        self.lb_theme_num.setText('' + num_list[0] + '~' + num_list[1] + '인')

    def inset_folium(self):
        layout = QVBoxLayout()
        layout.addWidget(self.webview)
        self.widget_map.setLayout(layout)
        map = folium.Map(location=[35.158450, 126.795422], zoom_start=16)
        marker = folium.Marker(location=[35.158450, 126.795422],
                               icon=folium.Icon(color='red', icon='key', prefix='fa')).add_to(map)
        marker.add_child(folium.Popup("방탈출 카페", min_width=100, max_width=100))
        # map.save('map.html')
        self.webview.setUrl(QUrl('file:///map.html'))
        self.webview.show()

    def email_content(self):
        self.r_email = self.lb_user_email.text()
        x = self.subscribe_table.selectedIndexes()
        row = x[0].row()
        column = x[0].column()
        selected_id = self.subscribe_table.item(row, column).text()
        print(f"selected_id : {selected_id}")

        To = f'{self.r_email}'
        e_content_1 = f"예약 테마 :  {self.ldt_theme.text()}."
        e_content_2 = f"예약 일시 : {self.ldt_date.text()}/{self.ldt_time.text()}"
        e_content_3 = f"예약 인원/가격 : {self.ldt_num.text()} {self.ldt_price.text()}"
        e_content_4 = f"예약 대표자 : {self.ldt_name.text()} {self.ldt_phone.text()}"
        title = f"[루시드 드림] {selected_id}님의 방탈출테마 예약내역 전송"

        html = f"""\
                <!DOCTYPE html>
                 <html lang="en">
                 <head>
                     <meta charset="UTF-8" />
                     <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                     <title>{title}</title>
                 </head>
                 <body>
                     <h4>안녕하세요. {selected_id} 님. </h4>
                     <p style="padding:5px 0 0 0;">{e_content_1} </p>
                     <p style="padding:5px 0 0 0;">{e_content_2} </p>
                     <p style="padding:5px 0 0 0;">{e_content_3} </p>
                     <p style="padding:5px 0 0 0;">{e_content_4} </p>
                 </body>
                 </html>
                 """

        msg = MIMEMultipart('alternative')
        msg['Subject'] = title
        msg['From'] = self.s_email
        msg['To'] = self.r_email
        html_msg = MIMEText(html, 'html')
        msg.attach(html_msg)

        return msg

    def send_reservation_email(self):
        # SMTP()서버의 도메인 및 포트를 인자로 접속하여 객체 생성
        server = smtplib.SMTP('smtp.gmail.com', 587)
        # SSL : SMTP_SSL('smtp.gmail.com', 465)

        # 접속 후 프로토콜에 맞춰 먼저 SMTP서버에 HELLO 메세지를 전송한다.
        server.ehlo()

        # 서버의 암호화 방식을 설정 -> TLS : Gmail 권장, SSL보다 향상된 보안
        server.starttls()

        # 서버 로그인
        server.login(self.s_email, self.s_pwd)
        # 이메일 발송
        try:
            server.sendmail(self.s_email, self.r_email, self.email_content().as_string())
            self.dlg_warning.set_dialog_type(1, "email_send")
            print("이메일 전송 성공")
        except:
            print("이메일 전송 실패")

        # 작업을 마친 후 SMTP와의 연결을 끊는다.
        server.quit()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.show()
    app.exec_()

