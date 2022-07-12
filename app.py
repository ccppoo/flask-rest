import json
from flask import Flask, jsonify, request
from mydb import DBWiterHandler
app = Flask(__name__)


@app.route('/room', methods=['GET'])
def a():
    # 방 보여달라고 하기
    return {
        'statusCode' : 200
    }

@app.route('/room/new', methods=['POST'])
def new_room():
    # 방 만들기
    return {
        'room_id' : '123'
    }

@app.route('/room/<string:room_id>', methods=['GET'])
def join_room(id : str):
    # 방 입장
    return {

    }

@app.route('/room/<string:room_id>', methods=['DELETE'])
def quit_room(id : str):
    # 방 퇴장
    return {

    }

@app.route('/room/<string:room_id>/chat', methods=['GET'])
def fetch_new_chats(room_id : str):
    # 방에서 새로운 채팅 가져오기
    print(room_id)
    '''
    count : (int)
    '''
    print(request.get_json())

    return {
        'statusCode' : 200
    }

@app.route('/room/<string:room_id>/chat', methods=['POST'])
def post_new_chat(room_id : str):
    # 방에 채팅 작성하기
    print(request.get_json())

    return {
        'statusCode' : 200
    }

if __name__ == '__main__':
    app.debug = True
    app.run(port=3333)