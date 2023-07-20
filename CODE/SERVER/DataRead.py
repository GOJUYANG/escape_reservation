import datetime
import sys
from PyQt5.QtWidgets import QApplication

import sqlite3 as sql3
import pandas as pd

class DataRea:
    def __init__(self):

        # --- 데이터베이스 연결
        self.conn = sql3.connect("data.db", check_same_thread=False)

        # --- 변수 초기화 및 설정
        self.now = datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S")

        # --- 함수호출

    def end_conn(self):  # db 종료
        self.conn.close()

    def commit_db(self):  # db 커밋
        self.conn.commit()

    def init_tables(self):

        # 회원정보 내역 테이블 생성 (!)자료형 입력하기(!)
        script_1 = f"""
        CREATE TABLE IF NOT EXISTS USER (
        'USER_NO' INTEGER PRIMARY KEY AUTOINCREMENT,
        'USER_ID' VARCHAR(20),
        'USER_PW' VARCHAR(16), 
        'USER_NM' VARCHAR(10),
        'USER_EMAIL' TEXT,
        'JOIN_DATE' CHAR(17),
        'USER_IMG' TEXT
        ); 
        """

        script_2 = f"""
        CREATE TABLE IF NOT EXISTS THEME_INFO (
        'TH_NM' VARCHAR(15) PRIMARY KEY UNIQUE,
        'TH_CONTENT' TEXT,
        'TH_LV' CHAR(5),
        'TH_NUM' CHAR(5),
        'TH_TIME' CHAR(5),
        'TH_IMG' TEXT,
        'TH_RESTIME' CHAR(10),
        'TH_PRICE' VARCHAR(10)
        );
        """

        script_3 = f"""
        CREATE TABLE IF NOT EXISTS RESERVATION (
        'RES_NO' INTEGER PRIMARY KEY AUTOINCREMENT,
        'USER_ID' VARCHAR(20),
        'USER_ADDR' TEXT,
        'RES_TH' VARCHAR(15),
        'RES_DATE' VARCHAR(20),
        'RES_TIME' CHAR(10),
        'RES_PRICE' VARCHAR(10),
        'RES_NUM' CHAR(5),
        'RES_REP_NM' VARCHAR(10),
        'RES_PHONE' CHAR(11),
        'RES_PAYTYPE' VARCHAR(10),
        FOREIGN KEY('USER_ID') REFERENCES 'USER'('USER_ID') );
        """

        script_4 = f"""INSERT INTO USER (USER_ID,USER_PW,USER_NM,USER_EMAIL,JOIN_DATE,USER_IMG)
         VALUES ('admin','1234','관리자','rhrnaka@gmail.com','{self.now}','../IMG/profile/manager.png');"""

        self.conn.execute(script_1)
        self.conn.execute(script_2)
        self.conn.execute(script_3)
        self.conn.execute(script_4)
        self.commit_db()
        self.end_conn()

    def return_df(self, c_type: str, tb_name: str):
        """return : 테이블"""
        sql = f"select {c_type} from {tb_name}"
        df = pd.read_sql(sql, self.conn)
        return df

    # 테이블 비우기
    def clear_table(self, col_name):
        self.conn.execute(f"delete from {col_name}")
        self.commit_db()

    # 원하는 테이블의 원하는 정보 가져오기
    def get_table(self, tb_name: str, user_id="", add_where=""):
        sql = f"select * from {tb_name}"

        if user_id:
            sql += f" where USER_ID = '{user_id}'"

        if add_where:
            if user_id:
                sql += " and"
            else:
                sql += " where"

            sql += add_where

        df = pd.read_sql(sql, self.conn)
        return df

    # 원하는 데이터에 정도 일괄 추가
    def insert_data(self, tb_name, data: dict, user_id=""):
        size = len(data)

        for k in data:
            sql = f"insert into {tb_name} ({k}) values (?)"
            if user_id != "":
                sql += f" where USER_ID = '{user_id}'"
            else:
                self.conn.execute(sql, data[k])
        self.commit_db()

# if __name__ == '__main__':
#     DATA = DataRead()