import socket
import json

# 챗봇 엔진 서버 접속 정보
host = "127.0.0.1"
port = 5050

# 클라이언트 프로그램 시작
while True:
    print("질문 :")
    query = input()
    if (quit == "exti"):
        exit(0)
    print("-"*40)

    # 챗봇 엔진 서버 연결
    mySocket = socket.socket()
    mySocket.connect((host, port))

    # 챗봇 엔진 질의 요청
    json_data = {
        'Query' : query,
        'BotType' : 'MyService'
    }
    message = json.dumps(json_data)
    mySocket.send(message.encode())

    # 챗봇 엔진 답변 출력
    data = mySocket.recv(2048).decode()
    ret_data = json.loads(data) # json 형태 문자열을 json 객체로 변환
    print("답변 :")
    print(ret_data['Answer'])
    print("\n")

# 챗본 엔진 서버 연결 소켓 닫기
mySocket.close()

