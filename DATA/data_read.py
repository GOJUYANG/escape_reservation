import datetime
import sys
from PyQt5.QtWidgets import QApplication

import sqlite3 as sql3
import pandas as pd

class DataRead:
    def __init__(self):

        # 데이터 베이스 연결
        self.conn = sql3.connect("data.db", check_same_thread=False)

        self.now = datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S")

    def commit_db(self):
        self.conn.commit()

    def init_tables(self):

        # 회원정보 내역 테이블 생성 (!)자료형 입력하기(!)
        script = f"""
        CREATE TABLE 'USER' (
        'USER_NO' INTEGER,
        'USER_ID' VARCHAR(20),
        'USER_PW', 
        'USER_NM',
        'USER_EMAIL',
        'JOIN_DATE',
        'USER_IMG',
        PRIMARY KEY('USER_NO' AUTOINCREMENT) );
        
        CREATE TABLE 'THEME_INFO' (
        '
        )

        CREATE TABLE 'RESERVATION' (
        )
                
        INSERT INTO USER VALUES ('admin','1234','관리자','rhrnaka@gamil.com','{self.now}','../IMG/profile/manager.png');
       
        """

        self.conn.executescript(script)

        self.commit_db()

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