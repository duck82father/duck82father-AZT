import sys
import os
from os import path
sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ))

from utils.Preprocess import Preprocess

sent = "내일 오전 10시에 짬뽕 주문하고 싶어ㅋㅋ"

# 전처리 객체 생성
cwd = os.getcwd()
tsvfile = os.path.join(cwd, 'utils', 'user_dic.tsv')
p = Preprocess(userdic=tsvfile)

# 형태소 분석기 실행
pos = p.pos(sent)

# 품사 태그와 같이 키워드 출력
ret = p.get_keywords(pos, without_tag=False)
print(ret)

x = p.get_wordidx_sequence(ret)
print(x)

# 품사 태그 없이 키워드 출력
ret = p.get_keywords(pos, without_tag=True)
print(ret)

