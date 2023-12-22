import sys
import os
from os import path
sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ))

import pymysql
import openpyxl
from config.DatabaseConfig import *

# 데이터 초기화
def all_clear_train_data(db):
    # 기존 학습 데이터 삭제
    sql = '''
        delete from chatbot_train_data
    '''
    with db.cursor() as cursor:
        cursor.execute(sql)

    sql = '''
        alter table chatbot_train_data AUTO_INCREMENT=1
    '''
    with db.cursor() as cursor:
        cursor.execute(sql)

# 데이터 추가
def insert_data(db, xls_row):
    intent, ner, query, answer, answer_img_url = xls_row

    sql = '''
        insert chatbot_train_data(intent, ner, query, answer, answer_image)
        values ("%s", "%s", "%s", "%s", "%s")
    ''' % (intent.value, ner.value, query.value, answer.value, answer_img_url.value)

    # 엑셀에서 불러온 cell 에 데이터가 없는 경우 null로 치환
    sql = sql.replace('None', 'Null')

    with db.cursor() as cursor:
        cursor.execute(sql)
        print('{} 저장'.format(query.value))
    
    db.commit()

cwd = os.getcwd()
train_file = os.path.join(cwd, 'train_tools', 'qna', 'train_data.xlsx')
#train_file = './train_data.xlsx'
db = None
try:
    db = pymysql.connect(
        host = DB_HOST,
        user = DB_USER,
        passwd = DB_PASSWORD,
        db = DB_NAME,
        port = DB_PORT,
        charset = 'utf8'
    )

    # 기존 학습 초기화
    all_clear_train_data(db)

    # 학습 엑셀 파일 불러오기
    wb = openpyxl.load_workbook(train_file)
    sheet = wb['Sheet1']
    for row in sheet.iter_rows(min_row=2):
        insert_data(db, row)
    
    wb.close()

except Exception as e:
    print(e)

finally:
    if db is not None:
        db.close()