import sys
import os
from os import path
sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ))
cwd = os.getcwd()
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

from utils.Preprocess import Preprocess
from models.intent.IntentModel import IntentModel

word2index_dic = os.path.join(cwd, 'train_tools', 'dict', 'chatbot_dict.bin')
userdic = os.path.join(cwd, 'utils', 'user_dic.tsv')
model = os.path.join(cwd, 'models', 'intent', 'intent_model.h5')

p = Preprocess(word2index_dic=word2index_dic, userdic=userdic)

intent = IntentModel(model_name=model, preprocess=p)

while True:
    query = input("입력 : ")
    predict = intent.predict_class(query)
    predict_label = intent.labels[predict]

    print(query)
    print("의도 예측 클래스 : ", predict)
    print("의도 예측 레이블 : ", predict_label)