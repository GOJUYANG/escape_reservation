import datetime
import sys
from PyQt5.QtWidgets import QApplication
from CODE.MAIN.DataClass import *

import sqlite3 as sql3
import pandas as pd
import re

class DataRead:
    def __init__(self):

        # --- 데이터베이스 연결
        self.conn = sql3.connect("../SERVER/data.db", check_same_thread=False)

        # --- 변수 초기화 및 설정
        self.now = datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S")

        # --- 함수호출
        # self.return_df('TH_NM', 'THEME_INFO')

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

    def return_df(self, c_type:str, tb_name:str):
        """return : THEME_INFO 테이블"""
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

    # 원하는 데이터에 정보 일괄 추가
    def insert_data(self, tb_name, data: dict, user_id=""):
        size = len(data)

        for k in data:
            sql = f"insert into {tb_name} ({k}) values (?)"
            if user_id != "":
                sql += f" where USER_ID = '{user_id}'"
            else:
                self.conn.execute(sql, data[k])
        self.commit_db()
        self.end_conn()

    def membership_id_check(self, data: ReqDuplicateCheck) -> PerDuplicateCheck:
        """클라이언트 중복 아이디 확인 요청 -> 서버 db에서 아이디 중복 여부 응답"""
        result: PerDuplicateCheck = PerDuplicateCheck(isExisited=True)
        sql = f"SELECT * FROM USER WHERE USER_ID = '{data.id_}'"
        row = pd.read_sql(sql, self.conn)

        if len(row) != 0:
            result.isExisited = True
        else:
            result.isExisited = False
        return result

    def eamil_check(self, data: ReqValidEmail) -> PerValidEmail:
        """클라이언트 이메일 주소 유효 확인 요청"""
        result: PerValidEmail = PerValidEmail(isValid=True)
        if re.match(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', data.r_email):
            result = PerValidEmail(True)
        else:
            result = PerValidEmail(False)
        return result

    def membership_regist(self, data: ReqJoin) -> PerJoin:
        result: PerJoin = PerJoin(True)
        try:
            sql = f"INSERT INTO USER (USER_ID, USER_PW, USER_NM, USER_EMAIL, JOIN_DATE, USER_IMG)" \
                  f"VALUES ('{data.id_}','{data.pw}','{data.nm}','{data.email}','{data.c_date}','{data.img}')"
            self.conn.execute(sql)
            self.conn.commit()

        except:
            self.conn.rollback()
            result.Success = False
        finally:
            self.conn.close()
        return result

    def login(self, data: ReqLogin) -> PerLogin:
        print("[ login ]")
        """클라이언트 로그인 요청 -> 서버 로그인 허가 """
        result: PerLogin = PerLogin(rescode=2, login_id=data.login_id)
        sql = f"SELECT * FROM USER WHERE USER_ID = '{data.login_id}' AND USER_PW = '{data.login_pw}'"
        print(sql)
        df = pd.read_sql(sql, self.conn)
        row = len(df)
        print("row",row)

        if row in [None, 0]:
            result.rescode = 0
        # 입력한 아이디와 비밀번호, db에서 가진 아이디와 비밀번호
        # elif data.id_ != row[1] or data.password != row[2]:
        #     result.rescode = 1
        else:
            result.rescode = 2
        return result

    def insert_message(self, data):
        print(f"[ 메세지 저장..]")
        self.conn.execute(f"insert into CHATROOM_{data.user_id} (SEND_ID, MSG_TYPE, MESSAGE, LAST_SEND_TIME)"
                          f" values (?,?,?,?)",
                          (data.user_id, data.msg_type, data.msg, data.send_time))
        self.commit_db()
        print(f" [메세지 저장 완료] ")
        self.end_conn()

    def save_subtb(self, data: ReqSubTheme) -> PerSubTheme:
        print("[ 구독 요청 저장 완료 ]")
        result: PerSubTheme = PerSubTheme(isSaved=True)
        try:
            self.conn.execute(f"insert into SUBSCRIBE (USER_ID, Req_Date, TH_NM, TH_TIME) "
                              f"values (?,?,?,?)",
                              (data.user_id, data.req_date, data.th_nm, data.th_time))
            self.commit_db()
            print("[ 구독 요청 저장 완료 ]")
        except:
            self.conn.rollback()
            result.Success = False
        finally:
            self.conn.close()
        return result

    def send_email(self, data: ResMngOk) -> PerEmailSend:
        result: PerEmailSend = PerEmailSend('')
        if data.e_type == '예약':
            result = PerEmailSend('reservation')
        elif data.e_type == '구독':
            result = PerEmailSend('subscribe')
        return result

    def save_restb(self, data: ReqResUserOK) -> PerResOk:
        print("[ 예약 내역 저장.. ]")
        result: PerResOk = PerResOk(savedone=True)
        try:
            self.conn.execute(f"insert into RESERVATION (USER_ID, USER_ADDR, Req_Date,"
                              f"RES_TH, RES_DATE, RES_TIME, RES_PRICE, RES_NUM, RES_REP_NM, RES_PHONE, RES_PAYTYPE) "
                              f"values (?,?,?,?,?,?,?,?,?,?,?)",
                              (data.user_id, data.user_addr, data.req_date,
                               data.th_nm, data.th_date, data.th_time, data.th_price,
                               data.th_num, data.th_phone, data.th_paytype))
            self.commit_db()
            print("[ 예약 내역 저장 완료 ]")
        except:
            self.conn.rollback()
            result.savedone = False
        finally:
            self.conn.close()
        return result

    def get_tables_starting_with(self, want:str, prefix:str):
        if want == 'part':
            df = pd.read_sql(f"select * from {prefix}")
            print(f"df : {df}")

        elif want == 'all':
            self.conn.execute("SELECT tbl_name FROM sqlite_master WHERE type='table' AND name LIKE ?", (prefix + '%',))
            table_names = [row[0] for row in self.conn.cursor().fetchall()]

            # df 로 만들지 고민해야하는 부분..
            for table_name in table_names:
                print("Table:", table_name)
                self.conn.execute("SELECT * FROM {}".format(table_name))
                rows = self.conn.cursor().fetchall()
                for row in rows:
                    print(row)

        self.end_conn()

    # 예약테이블 행 수정
    def update_restb(self, data: ReqResFix) -> PerResfix:
        result: PerResfix = PerResfix(isfix=True)
        self.conn.execute(f"update RESERVATION SET "
                          f"TH_PRICE = {data.th_price},"
                          f" TH_NUM = {data.th_num},"
                          f" TH_NAME = {data.th_name},"
                          f" TH_PHONE = {data.th_phone} "
                          f"where USER_ID = {data.user_id}")
        self.commit_db()
        self.end_conn()
        return result

    # 예약테이블 행 삭제
    def delete_restb(self, data: ReqResCancel) -> PerResCancel:
        result: PerResCancel = PerResCancel(iscancel=True)
        self.conn.execute(f"delete from RESERVATION "
                          f"WHERE USER_ID = {data.user_id}")

        self.commit_db()
        self.end_conn()
        return result

if __name__ == '__main__':
    App = QApplication(sys.argv)
    DATA = DataRead()
    App.exec()

    # 유저만 필요한 부분, 관리자는 필요없다.
    # self.insert_message(ReqUserChat(f"'{data.nm}'님이 입장했습니다."))