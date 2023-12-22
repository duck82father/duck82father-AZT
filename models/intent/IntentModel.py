import tensorflow as tf
from keras.models import Model, load_model
from keras import preprocessing

import sys
import os
from os import path
sys.path.append(path.dirname( path.dirname( path.abspath( path.dirname( path.abspath(__file__))))))

# 의도 분류 모델 모듈
class IntentModel:
    def __init__ (self, model_name, preprocess):

        # 의도 클래스 레이블
        self.labels = {0:"인사", 1:"욕설", 2:"주문", 3:"예약", 4:"기타", 5:"다른 문제", 6:"힌트"}

        # 의도 분류 모델 불러오기
        self.model = load_model(model_name)

        # 챗봇 Preprocess 객체
        self.p = preprocess


    # 의도 클래스 예측
    def predict_class(self, query):
        # 형태소 분석
        pos = self.p.pos(query)
        
        # 문장 내 키워드 추출
        keywords = self.p.get_keywords(pos, without_tag = True)
        sequences = [self.p.get_wordidx_sequence(keywords)]

        # 단어 시퀀스 벡터 크기
        from config.GlobalParams import MAX_SEQ_LEN

        # 패딩 처리
        padded_seqs = preprocessing.sequence.pad_sequences(sequences, maxlen=MAX_SEQ_LEN, padding='post')

        predict = self.model.predict(padded_seqs)
        predict_class = tf.math.argmax(predict, axis=1)
        return predict_class.numpy()[0]
    

if __name__ == "__main__":

    print(path.dirname( path.dirname( path.abspath( path.dirname( path.abspath(__file__))))))
    import config
    print(dir(config))

    from config.GlobalParams import MAX_SEQ_LEN
    print(MAX_SEQ_LEN)