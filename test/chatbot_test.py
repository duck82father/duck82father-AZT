import sys
import os
from os import path
sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ))
cwd = os.getcwd()
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

from config.DatabaseConfig import *
from utils.Database import Database
from utils.Preprocess import Preprocess

# 전처리 객체 생성
word2index_dic = os.path.join(cwd, 'train_tools', 'dict', 'chatbot_dict.bin')
userdic = os.path.join(cwd, 'utils', 'user_dic.tsv')
p = Preprocess(word2index_dic=word2index_dic, userdic=userdic)

# 질문/답변 학습 DB 연결 객체 생성
db = Database(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, port=DB_PORT, db_name=DB_NAME)
db.Connect()

# 원문
query = "오전에 탕수육 10개 주문합니다."

# 의도 파악
from models.intent.IntentModel import IntentModel
intentmodel = os.path.join(cwd, 'models', 'intent', 'intent_model.h5')
intent = IntentModel(model_name=intentmodel, preprocess=p)
predict = intent.predict_class(query)
intent_name = intent.labels[predict]

# 개체명 인식
from models.ner.NerModel import NerModel
nermodel = os.path.join(cwd, 'models', 'ner', 'ner_model.h5')
ner = NerModel(model_name=nermodel, preprocess=p)
predicts = ner.predict(query)
ner_tags = ner.predict_tags(query)

print("질문 : ", query)
print("=" * 40)
print("의도 파악 : ", intent_name)
print("개체명 인색 : ", predicts)
print("답변 검색에 필요한 NER 태그 : ", ner_tags)
print("=" * 40)

# 답변 검색
from utils.FindAnswer import FindAnswer

try :
    f = FindAnswer(db)
    answer_text, answer_image = f.search(intent_name, ner_tags)
    answer = f.tag_to_word(predicts, answer_text)
except:
    answer = "죄송해요, 무슨 말인지 모르겠어요."

print("답변 : ", answer)

db.close()