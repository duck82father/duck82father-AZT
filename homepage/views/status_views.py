from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect

from homepage import db
from homepage.models import azquiz, Solved
from homepage.views.auth_views import login_required
from homepage.client import chatbot_client

import re

bp = Blueprint('status', __name__, url_prefix='/status')

def insertAnswerCheckToDB (quiznumber):
    solved_record = Solved(user_id=g.user.id, quiz_id=quiznumber)    
    answer = azquiz.query.get(quiznumber).answer
    db.session.add(solved_record)
    db.session.commit()
    return answer

def countSolved ():
    solved_count = Solved.query.filter_by(user_id=g.user.id).count()
    if solved_count % 10 == 0:
        return solved_count
    else:
        solved_count = 0
        return

@bp.route('/show/', methods=('GET', 'POST'))
@login_required
def show():
    solved = Solved.query.filter_by(user_id=g.user.id).all()
    quizs = azquiz.query
    solved_quiz_ids = []
    for solve in solved:
        solved_quiz_ids.append(solve.quiz_id)
    return render_template('status.html', quizs=quizs, solved_quiz_ids=solved_quiz_ids)

@bp.route('/show/api/endpoint', methods=['POST'])
def api_endpoint():
    data = request.json  # JSON 형식의 데이터를 받기 위해 request.json 사용
    
    requestkey, quiznumber = data['key'], data['quiznumber']    
    result = re.findall(r'\d+', requestkey)
    order_result = re.findall(r'주문', requestkey)
    answer = None
    solved_count = 0

    print("status : requestkey = {}, quiznumber = {}".format(requestkey, quiznumber))

    if order_result == ['주문']:
        if order_result[0] == '주문':
            result = chatbot_client(requestkey)
            resulttype = "order"

    elif (result != [] and requestkey[-1:] == "번") or (result != [] and requestkey[-2:] == "문제") or (result != [] and requestkey[-1:] == "qjs"):
        result = int(result[0])
        if result > 120:
            result = "문제가 없습니다. [ 범위 1 ~ 120번 ]"
            resulttype = "order" 
        else: 
            resulttype = "quiz"

    elif int(quiznumber) > 0 :
        target_quiz = azquiz.query.get(quiznumber)
        if "힌트" in requestkey or "hint" in requestkey.lower():
            result = target_quiz.hint
            resulttype = "order"
        else:
            if requestkey == target_quiz.answer:
                if Solved.query.filter_by(user_id=g.user.id, quiz_id=quiznumber).first() != None:
                    result = '이미 맞춘 문제입니다👍'
                    resulttype = "alreadySolved"
                    answer = azquiz.query.get(quiznumber).answer
                else:
                    result = '<b class="fw-bold">정답</b>입니다🥳'
                    resulttype = "answer"
                    answer = insertAnswerCheckToDB (quiznumber)
                    solved_count = countSolved ()
            else :
                result = "다시 한 번 고민해보세요!"
                resulttype = "order"
    
    else :      
        result = chatbot_client(requestkey)
        resulttype = "order"
    
    return {'result':f'{result}', 'resulttype':f'{resulttype}',
            'answer':f'{answer}', 'solvedCount':f'{solved_count}'}