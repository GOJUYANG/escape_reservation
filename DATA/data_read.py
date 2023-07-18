import sys
from PyQt5.QtWidgets import QApplication

import sqlite3 as sql3
import pandas as pd

class DataRead:
    def __init__(self):
        self.conn = sql3.connect("data.db", check_same_thread=False)

    def init_tables(self):

        # 회원정보 내역 테이블
        self.conn.executescript("""
        CREATE TABLE 'USER' (
        'USER_NO')""")

    def db_create(self, user_id):
        pass

    def db_insert(self, t_type):
        pass

    def db_update(self, t_type):
        pass

    def db_delete(self, t_type):
        pass

    def db_drop(self, t_type):
        pass

if __name__ == '__main__':
    App = QApplication(sys.argv)
    DATA = DataRead()
    DATA.show()
    App.exec()