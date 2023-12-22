import sys
import os
from os import path
sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ))
cwd = os.getcwd()
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

from utils.Preprocess import Preprocess
from models.ner.NerModel import NerModel

word2index_dic = os.path.join(cwd, 'train_tools', 'dict', 'chatbot_dict.bin')
userdic = os.path.join(cwd, 'utils', 'user_dic.tsv')
nermodel = os.path.join(cwd, 'models', 'ner', 'ner_model.h5')

p = Preprocess(word2index_dic=word2index_dic, userdic=userdic)
ner = NerModel(model_name=nermodel, preprocess=p)
query = '짬뽕 1그릇 주문이요'
predicts = ner.predict(query)
tags = ner.predict_tags(query)
print(predicts)
print(tags)

