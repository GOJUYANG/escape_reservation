from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from CODE.SCREEN.Font import Font

class AddChat(QDialog):
    """친구 방 추가하는 부분"""
    def __init__(self):
        super().__init__()
        # 친구 목록 아이디 딕셔너리
        self._all_friend = dict()

        # --- 화면 설정
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.set_style()
        self.init_ui()

    def init_ui(self):
        # --- 화면 객체 생성 및 크기 조정
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(9, 9, 9, 9)

        # --- 방 이름 입력 영역
        _head_layout = QHBoxLayout()
        _head_layout.setContentsMargins(6, 6, 6, 6)
        self._lbl_chat_name = QLabel()
        self._lbl_chat_name.setText("채팅방 이름")
        self._lbl_chat_name.setFont(Font.title(5))
        _head_layout.addWidget(self._lbl_chat_name)
        self._chat_name_edit = QLineEdit()
        _head_layout.addWidget(self._chat_name_edit)
        layout.addLayout(_head_layout)

        # --- 친구 목록 스크롤 영역
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_contents = QWidget()
        _scroll_layout = QVBoxLayout(self.scroll_contents)
        self.scroll_area.setWidget(self.scroll_contents)
        layout.addWidget(self.scroll_area)

        # --- 선택 인원 합계 출력 영역
        label1 = QLabel('채팅방 총 원: ')
        label1.setFont(Font.text(3))
        self._lbl_total_num = QLabel('0명')
        self._lbl_total_num.setFont(Font.text(3))
        spacer2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        h_layout = QHBoxLayout()
        h_layout.addWidget(label1)
        h_layout.addItem(spacer2)
        h_layout.addWidget(self._lbl_total_num)
        h_layout.setContentsMargins(8, 0, 16, 4)
        layout.addLayout(h_layout)

        # --- 버튼 박스 영역
        _btn_layout = QHBoxLayout()
        _btn_accept = QPushButton('방 만들기')
        _btn_accept.setFont(Font.text(3))
        _btn_accept.setFixedHeight(50)
        _btn_accept.clicked.connect(self.accept)
        _btn_layout.addWidget(_btn_accept)
        _btn_reject = QPushButton('취소')
        _btn_reject.setFont(Font.text(3))
        _btn_reject.setFixedHeight(50)
        _btn_reject.clicked.connect(self.reject)
        _btn_layout.addWidget(_btn_reject)
        layout.addLayout(_btn_layout)

        # -- 메인 레이아웃 설정
        self.setLayout(layout)

    def set_member_list(self, t_df):
        _scroll_layout = self.scroll_contents.layout()
        # 스크롤 영역 아이템 추가
        # for i, data in t_df.iterrows():
            # item = ListItem(data["F_ID"], data["USER_NM"], data["USER_STATE"], data["USER_IMG"])
            # _scroll_layout.addWidget(item.frame)
            # _scroll_layout.addLayout(item.add_checkbox())
            # self._all_friend[i] = [item.item_id, item.item_nm]

        # 스크롤 내부 스페이서 추가
        _spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Expanding)
        _scroll_layout.addSpacerItem(_spacer)

        # -- 체크박스 체크될 때마다 라벨 변하는 부분 추가
        self.checkboxes = self.findChildren(QCheckBox)
        for checkbox in self.checkboxes:
            checkbox.clicked.connect(self.change_cnt_label)

    def change_cnt_label(self):
        """체크박스 누를 때마다 라벨 변하는 부분"""
        count = sum(checkbox.isChecked() for checkbox in self.checkboxes)
        self._lbl_total_num.setText(f'{str(count)}명')

    def set_style(self):
        """화면 스타일시트 추가"""
        self.setStyleSheet("* { background-color: white; }"
                           "QPushButton { background-color: rgb(248,228,208); border-radius: 25px; }"
                           "QLineEdit { border: 1px solid; border-radius: 8px; padding: 8px 12px;}")
        self.setFixedSize(420, 750)
        self.setWindowTitle("방 추가 화면")

    def reset_dialog(self):
        self._chat_name_edit.clear()
        self._lbl_total_num.setText("0명")
        # for checkbox in self.checkboxes:
        #     checkbox: QCheckBox
        #     checkbox.setChecked(False)

    @property
    def chat_name(self):
        """채팅방 이름"""
        return self._chat_name_edit.text()

    @property
    def members(self):
        """채팅방 멤버"""
        member_id = list()
        member_name = list()

        for i, check in enumerate(self.checkboxes):
            if check.isChecked():
                member_id.append(self._all_friend[i][0])
                member_name.append(self._all_friend[i][1])
        return member_id, member_name


if __name__ == '__main__':
    app = QApplication([])
    dialog = AddChat()
    dialog.show()
    app.exec_()
