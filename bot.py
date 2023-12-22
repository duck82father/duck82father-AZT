import sys
import os
from os import path
sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ))
cwd = os.getcwd()
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

import threading
import json

from config.DatabaseConfig import *
from utils.Database import Database
from utils.BotServer import BotServer
from utils.Preprocess import Preprocess
from models.intent.IntentModel import IntentModel
from models.ner.NerModel import NerModel
from utils.FindAnswer import FindAnswer

# 전처리 객체 생성
word2index_dic = os.path.join(cwd, 'train_tools', 'dict', 'chatbot_dict.bin')
userdic = os.path.join(cwd, 'utils', 'user_dic.tsv')
p = Preprocess(word2index_dic=word2index_dic, userdic=userdic)

# 의도 파악 모델
intentmodel = os.path.join(cwd, 'models', 'intent', 'intent_model.h5')
intent = IntentModel(model_name=intentmodel, preprocess=p)

# 개체명 인식 모델
nermodel = os.path.join(cwd, 'models', 'ner', 'ner_model.h5')
ner = NerModel(model_name=nermodel, preprocess=p)

def to_client(conn, addr, prams):
    db = prams['db']
    try:
        db.Connect()

        # 데이터 수신
        read = conn.recv(2048)  # 수신 데이터가 있을 때까지 블로킹
        print("="*20)
        print("Connection from : %s"% str(addr))

        if read is None or not read:
            # 클라이언트 연결이 끊어지거나 오류가 있는 경우
            print("클라이언트 연결 끊어짐")
            exit(0) # 스레드 강제 종료

        # json 데이터로 변환
        recv_json_data = json.loads(read.decode())
        print("데이터 수신 : ", recv_json_data)
        query = recv_json_data['Query']

        # 의도 파악
        intent_predict = intent.predict_class(query)
        intent_name = intent.labels[intent_predict]

        print(intent_predict, intent_name)

        # 개체명 파악
        ner_predicts = ner.predict(query)
        ner_tags = ner.predict_tags(query)

        print(ner_predicts, ner_tags)

        # 답변 검색
        if intent_predict != 0 and ner_tags == None:
            answer = "죄송해요 무슨 말인지 모르겠어요. 조금 더 공부할게요"
            answer_image = None
        else: 
            try:
                f = FindAnswer(db)
                answer_text, answer_image = f.search(intent_name, ner_tags)
                answer = f.tag_to_word(ner_predicts, answer_text)
            except:
                answer = "죄송해요 무슨 말인지 모르겠어요. 조금 더 공부할게요"
                answer_image = None

        send_json_data_str = {
            "Query" : query,
            "Answer" : answer,
            "AnswerImageUrl" : answer_image,
            "Intent" : intent_name,
            "NER" : str(ner_predicts)
        }
        message = json.dumps(send_json_data_str)    # json 객체를 전송 가능한 문자열로 변환
        conn.send(message.encode()) # 응답 전송

    except Exception as ex:
        print(ex)

    finally:
        if db is not None:
            db.close()
        conn.close()


if __name__ == '__main__':
    # 질문/답변 학습 db 연결 객체 생성

    db = Database(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, port=DB_PORT, db_name=DB_NAME)
    print("DB 접속")

    # 봇 서버 동작
    port = 5050
    listen = 100
    bot = BotServer(port, listen)
    bot.create_sock()
    print("bot start")

    while True:
        conn, addr = bot.ready_for_client()
        params = {
            "db" : db
        }

        client = threading.Thread(target=to_client, args=(
            conn,   # 클라이언트 연결 소켓
            addr,   # 클라이언트 연결 주소 정보
            params  # 스레드 함수 파라미터
        ))

        client.start()