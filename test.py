# def delete_fav_db(self, rstrn_="", place_=""):
#     df = pd.read_sql(f"select * from TB_FAV", self.conn)
#
#     if rstrn_ == "":
#         condition = df['PLACE_NM'] == f'{place_}'
#     elif place_ == "":
#         condition = df['RSTRN_NM'] == f'{rstrn_}'
#     else:
#         condition = (df['RSTRN_NM'] == f'{rstrn_}') & (df['PLACE_NM'] == f'{place_}')

#데이터프레임(DataFrame) 필터링
#     df = df[~condition]
#     df.to_sql('TB_FAV', self.conn, if_exists='replace', index=False)

join_data = ['a', 'b', 'c', 'd']
dict_: dict = {}

dict_['USER_ID'] = join_data[0]
dict_['USER_PW'] = join_data[0]
dict_['USER_NM'] = join_data[0]
dict_['USER_EMAIL'] = join_data[0]

print(dict_)
