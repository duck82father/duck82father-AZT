import sys
import os
from os import path
sys.path.append(path.dirname(path.abspath(path.dirname(path.abspath(path.dirname(__file__))))))
cwd = os.getcwd()

import pickle
from utils.Preprocess import Preprocess

# 단어 사전 불러오기
bin_file = os.path.join(cwd, 'train_tools', 'dict', 'chatbot_dict.bin')
f = open(bin_file, "rb")
word_index = pickle.load(f)
f.close()

sent = "내일 오전 10시에 탕수육 주문하고 싶 ㅋㅋ"

# 전처리 객체 생성
tsvfile = os.path.join(cwd, 'utils', 'user_dic.tsv')
p = Preprocess(userdic=tsvfile)

# 형태소 분석기 실행
pos = p.pos(sent)

# 품사 태그 없이 키워드 출력
keywords = p.get_keywords(pos, without_tag=True)
for word in keywords:
    try:
        print(word, word_index[word])
    except KeyError:
        # 해당 단어가 사전에 없어 OOV처리된 단어(?)
        print(word, word_index['OOV'])

