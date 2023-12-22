import sys
from os import path
sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ))

import pymysql
from config.DatabaseConfig import *

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

    # 테이블 생성 SQL 정의
    sql = '''
        create table if not exists `chatbot_train_data` (
        `id` int unsigned not null auto_increment,
        `intent` varchar(45) null,
        `ner` varchar(1024) null,
        `query` text null,
        `answer` text not null,
        `answer_image` varchar(2048) null,
        primary key(`id`)
    ) engine = InnoDB default charset = utf8
    '''

    # 테이블 생성
    with db.cursor() as cursor:
        cursor.execute(sql)

except Exception as e:
    print(e)

finally:
    if db is not None:
        db.close()