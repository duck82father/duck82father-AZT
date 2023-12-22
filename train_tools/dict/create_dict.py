# 챗봇에서 사용하는 사전 파일 생성

import sys
import os
from os import path
sys.path.append(path.dirname(path.abspath(path.dirname(path.abspath(path.dirname(__file__))))))
cwd = os.getcwd()

from utils.Preprocess import Preprocess
from keras import preprocessing
import pickle


# 말뭉치 데이터 읽어오기
def read_corpus_data(filename):
    with open(filename, 'r', encoding='UTF8') as f:
        data = [line.split('\t') for line in f.read().splitlines()]
        data = data[1:]
    return data

# 말뭉치 데이터 가져오기
txt_file = os.path.join(cwd, 'train_tools', 'dict', 'corpus.txt')
corpus_data = read_corpus_data(txt_file)

# 말뭉치 데이터에서 키워드만 추출하여 사전 리스트 생성
p = Preprocess()
dict = []
for c in corpus_data:
    pos = p.pos(c[1])
    for k in pos:
        dict.append(k[0])

# 사전에 사용될 word2index 생성 / 사전에 첫 번째 인덱스에서 OOV 사용
tokenizer = preprocessing.text.Tokenizer(oov_token='OOV')
tokenizer.fit_on_texts(dict)
word_index = tokenizer.word_index

# 사전 파일 생성
bin_file = os.path.join(cwd, 'train_tools', 'dict', 'chatbot_dict.bin')
f = open(bin_file, "wb")
try :
    pickle.dump(word_index, f)
except Exception as e:
    print(e)
finally:
    f.close()