from typing import List
import tensorflow as tf
from fastapi import WebSocket, APIRouter
from fastapi.responses import HTMLResponse
from keras_preprocessing.sequence import pad_sequences
from starlette.websockets import WebSocketDisconnect
from keras.models import load_model
from app.config.global_params import MAX_SEQ_LEN
from app.config.path import dir_path
from app.trains.chatbot.food_preprocess import Preprocess

router = APIRouter()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/chatbot/ws/${client_id}`);
            ws.onmessage = function(event) {
                alert(" 1 ")
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                alert(" 2 ")
                message.appendChild(content)
                alert(" 3 ")
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        print(" ## send_personal_message ## ")
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        print(" ## broadcast ## ")
        for connection in self.active_connections:
            print(" ## for in broadcast ## ")
            await connection.send_text(message)


manager = ConnectionManager()


@router.get("")
async def get():
    return HTMLResponse(html)


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"Client Ask: {data}", websocket)
            # res = food_intent2(data)
            await manager.broadcast(f"Server #{client_id} Answer: Good")
            print(" ###### end ######### ")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")


def food_intent(query: str):
    p = Preprocess(word2index_dic=f'{dir_path("train_tools/dict")}/chatbot_dict.bin',
                   userdic=f'{dir_path("train_tools/dict")}/user_dic.tsv')
    print(f"query : {query}")
    intent = IntentModel2(model_name=f"{dir_path('models/chatbot')}/intent_model.h5", proprocess=p)
    predict = intent.predict_class(query)
    print("의도 예측 클래스 : ", predict)
    predict_label = intent.labels[predict]
    print("의도 예측 레이블 : ", predict_label)
    return predict_label

def food_intent2(query: str):

    print(f"query 2: {query}") # query = "오늘 탕수육 주문 가능한가요?"
    intent_labels = {0: "인사", 1: "욕설", 2: "주문", 3: "예약", 4: "기타"}

    model = load_model(f'{dir_path("models/chatbot")}/intent_model.h5')
    print("intent 다음 ...")
    p = Preprocess(word2index_dic=f'{dir_path("train_tools/dict")}/chatbot_dict.bin',
                   userdic=f'{dir_path("train_tools/dict")}/user_dic.tsv')
    pos = p.pos(query)
    print(f"pos ...{pos}")
    keywords = p.get_keywords(pos, without_tag=True)
    print(f"keywords ...{keywords}")
    seq = p.get_wordidx_sequence(keywords)
    print(f"seq ...{seq}")
    sequences = [seq]
    print(f"sequences ...{sequences}")
    # 단어 시퀀스 벡터 크기
    padded_seqs = pad_sequences(sequences, maxlen=MAX_SEQ_LEN, padding='post')
    print(f"padded_seqs ...{padded_seqs}")
    predict = model.predict(padded_seqs)
    print("의도 예측 점수 : ", predict)
    predict_class = tf.math.argmax(predict, axis=1)
    print("의도 예측 클래스 : ", predict_class.numpy())
    res = intent_labels[predict_class.numpy()[0]]
    print(f"의도 결과  : {res}")
    return res


class IntentModel2:
    def __init__(self, model_name, proprocess):
        # 의도 클래스 별 레이블
        self.labels = {0: "인사", 1: "욕설", 2: "주문", 3: "예약", 4: "기타"}

        # 의도 분류 모델 불러오기
        self.model = load_model(model_name)

        # 챗봇 Preprocess 객체
        self.p = proprocess

    # 의도 클래스 예측
    def predict_class(self, query):
        # 형태소 분석
        pos = self.p.pos(query)

        # 문장내 키워드 추출(불용어 제거)
        keywords = self.p.get_keywords(pos, without_tag=True)
        sequences = [self.p.get_wordidx_sequence(keywords)]

        # 단어 시퀀스 벡터 크기

        # 패딩처리
        padded_seqs = pad_sequences(sequences, maxlen=MAX_SEQ_LEN, padding='post')

        predict = self.model.predict(padded_seqs)
        predict_class = tf.math.argmax(predict, axis=1)
        return predict_class.numpy()[0]