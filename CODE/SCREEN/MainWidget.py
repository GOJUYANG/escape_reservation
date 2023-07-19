import random
import datetime
import folium
from folium import Marker

from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import QUrl, Qt
from PyQt5 import QtWebEngineWidgets

from CODE.SCREEN.UI_MainWidget import Ui_MainWindow
from CODE.SCREEN.UI_Login import Ui_Login
from CODE.SERVER.DataRead import DataRead

from CODE.CLIENT.Client import Client

class Theme():
    def __init__(self, num, list_NM, list_IMG):
        # 사용자 정의 QWidget 제작

        theme_container = QWidget()
        theme_container.setFixedSize()



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

        # --- qwebview 객체 생성
        self.webview = QtWebEngineWidgets.QWebEngineView(self.widget_map)
        self.webview.resize(591, 411)

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

        # self.screen_login = LOGIN()
        # self.screen_login.show()

        # --- DB연결
        self.db = DataRead()

        # --- 함수 호출
        self.widget_clicked()
        self.inset_folium()

    def widget_clicked(self):
        self.widget_theme.mousePressEvent = lambda e, name='theme': self.mousePressEvent(e, name)
        self.widget_reservation.mousePressEvent = lambda e, name='reservation': self.mousePressEvent(e, name)
        self.widget_folium.mousePressEvent = lambda e, name='folium': self.mousePressEvent(e, name)
        self.widget_request.mousePressEvent = lambda e, name='request': self.mousePressEvent(e, name)

    def mousePressEvent(self, e, name):
        if name == 'theme':
            self.Client_stack.setCurrentIndex(0)
        elif name == 'reservation':
            self.Client_stack.setCurrentIndex(1)
        elif name == 'folium':
            self.Client_stack.setCurrentIndex(2)
        elif name == 'request':
            self.Client_stack.setCurrentIndex(3)

    def insert_theme(self):
        theme_df = self.db.return_df('*', 'THEME_INFO')
        list_NM = theme_df.TH_NM.tolist()
        list_IMG = theme_df.TH_IMG.tolist()
        num = len(list_NM)
        self.theme = Theme(num, list_NM, list_IMG)


    def inset_folium(self):
        layout = QVBoxLayout()
        layout.addWidget(self.webview)
        self.widget_map.setLayout(layout)
        map = folium.Map(location=[35.158450, 126.795422], zoom_start=14)
        marker = folium.Marker(location=[35.158450, 126.795422], icon=folium.Icon(icon='marker')).add_to(map)
        marker.add_child(folium.Popup("방탈출 카페", min_width=100, max_width=100))
        map.save('map.html')
        self.webview.setUrl(QUrl('file:///map.html'))
        self.webview.show()



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.show()
    app.exec_()

