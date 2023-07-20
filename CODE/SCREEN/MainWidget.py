import random
import datetime
import folium
from folium import Marker

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QMainWindow, QApplication
from PyQt5.QtGui import QPixmap

from PyQt5.QtCore import QUrl, Qt
from PyQt5 import QtWebEngineWidgets

from CODE.SCREEN.UI_MainWidget import Ui_MainWindow
from CODE.SCREEN.UI_Login import Ui_Login
from CODE.SERVER.DataRead import DataRead

from CODE.CLIENT.Client import Client


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


class LOGIN(QWidget, Ui_Login):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # --- 기초값 설정
        self.saved_id: str = ''

        # --- 서버 연결
        self.client = Client()

        # --- DB연결
        self.db = DataRead()

        # ---버튼 연결
        self.btn_membership.clicked.connect(lambda _, index=1: self.move_page(index))
        self.btn_join_ship.clicked.connect(self.check_membership_info)
        self.btn_login_exit.clicked.connect(self.shut_down)
        self.radio_id_save.toggled.connect(self.save_id)

        # self.btn_join_login.clicked.connect(self.move_main)

        # ---함수 호출
        self.init_ui()

    def init_ui(self):
        from PyQt5.QtCore import Qt
        self.setWindowFlags(Qt.FramelessWindowHint)

        if self.save_id()[0]:
            self.lb_login_id.setText(self.saved_id)
        else:
            pass

    def shut_down(self):
        self.close()

    # --함수
    def move_page(self, index):
        """stackedwidget 페이지 이동"""
        self.stackedWidget.setCurrentIndex(index)

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

        # # 이메일 인증 확인
        elif not self.check_email():
            self.dlg_warning.set_dialog_type(1, "email_no_check")
            self.dlg_warning.exec()

        # 닉네임 확인
        elif not self.check_nickname_condition()[0]:
            self.dlg_warning.set_dialog_type(1, self.check_nickname_condition()[1])
            self.dlg_warning.exec()

        # 아이디 중복확인 진행 여부
        elif not self.use_id_check:
            self.dlg_warning.set_dialog_type(1, "used_id_no_check")
            self.dlg_warning.exec()

        else:
            self.user_id = id_
            # self.client.send(클라이언트요청데이터)
            self.move_page(0)

    def save_id(self):
        bool_ = self.radio_id_save.isChecked()
        if bool_:
            self.saved_id = self.lb_login_id.text()
            return True, self.saved_id
        else:
            self.saved_id = ''
            return True, self.saved_id

class MainWindow(QMainWindow, Ui_MainWindow, Ui_Login):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.res_available = True
        self.mouse_x: int = 0
        self.mouse_y: int = 0

        # --- DB연결
        self.db = DataRead()
        self.theme_df = self.db.return_df('*', 'THEME_INFO')

        # --- 클래스 호출
        # self.screen_login = LOGIN()
        # self.screen_login.show()

        # --- qwebview 객체 생성
        self.webview = QtWebEngineWidgets.QWebEngineView(self.widget_map)
        self.webview.resize(591, 411)

        # --- 함수 호출
        self.widget_clicked()
        self.inset_folium()
        self.insert_theme()
        self.label_clicked()
        self.insert_single_theme(0)

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
            self.Client_stack.setCurrentIndex(2)
            list_frame[0].hide()
            list_frame[1].hide()
            list_frame[2].show()
            list_frame[3].hide()
        elif name == 'request':
            self.Client_stack.setCurrentIndex(3)
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

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.show()
    app.exec_()

