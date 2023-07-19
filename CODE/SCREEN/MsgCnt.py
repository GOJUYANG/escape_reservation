from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

from CODE.SCREEN.Font import Font


class NoMsgCnt:
    def __init__(self, cnt=0):
        self._lbl_cnt = QLabel()

        self._lbl_cnt.setFont(Font.text(3))
        self._lbl_cnt.setFixedSize(20,20)
        self._lbl_cnt.setAlignment(Qt.AlignCenter)
        self._lbl_cnt.setStyleSheet("background-color:rgb(248,228,208);border-radius:10px")

        self.set_count(cnt)

    @property
    def label(self):
        return self._lbl_cnt

    def set_count(self, t_cnt:int):
        self._lbl_cnt.setText(f"{t_cnt}")
        if t_cnt:
            self._lbl_cnt.setVisible(True)
        else:
            self._lbl_cnt.setVisible(False)