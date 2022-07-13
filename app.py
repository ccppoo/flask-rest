import json
from flask import Flask, jsonify, request
from mydb import DBWiterHandler
import datetime
from gen_sample_chat import *
from chat_type import Chat_Data
from dataclasses import asdict

DBWriter = DBWiterHandler()
app = Flask(__name__)


@app.route('/room', methods=['GET'])
def a():
    # 방 ID 불러오기

    room_uuid_list = DBWriter.get_room_list()
    return {
        'statusCode' : 200,
        'room_uuid_list': room_uuid_list
    }

@app.route('/room/new', methods=['POST'])
def new_room():
    # 방 만들기

    req = request.get_json()
    room_name = req['room_name']
    room_uuid = DBWriter.make_new_room(room_name)

    return {
        'statusCode': 200,
        'room_uuid': room_uuid
    }

@app.route('/room/<string:room_id>', methods=['GET'])
def join_room(id : str):
    # 방 입장
    return {
        'statusCode': 200,

    }

@app.route('/room/<string:room_id>', methods=['DELETE'])
def quit_room(id : str):
    # 방 퇴장
    return {
        'statusCode': 200
    }

@app.route('/room/<string:room_id>/chat', methods=['GET'])
def fetch_new_chats(room_id : str):
    # 방에서 새로운 채팅 가져오기
    # print(room_id)
    '''
    count : (int)
    '''
    req = request.get_json()
    chats = DBWriter.get_chat(room_id, req['count'])
    
    return {
        'statusCode' : 200,
        'chats' : [
            asdict(x) for x in chats
        ]
    }

@app.route('/room/<string:room_id>/chat', methods=['POST'])
def post_new_chat(room_id : str):
    # 방에 채팅 작성하기
    # print(request.get_json())
    req = request.get_json()


    curtimestamp = datetime.datetime.now(tz=TZ_ko()).replace(microsecond=0)
    cd = Chat_Data(
        None,
        str(curtimestamp),
        req['member_nickname'],
        req['member_uuid'],
        req['chat_content'],
        req['media_type'],
        req['message_state']
    )
    
    DBWriter.put_chat(room_id, cd.commit())

    return {
        'statusCode' : 200,
        'room_uuid' : room_id
    }

if __name__ == '__main__':
    app.debug = True

    # fakes, fake_room_uuid = gen_chat(5, 50)
    # print(f'{fake_room_uuid=}')
    # DBWriter._make_chat_table(fake_room_uuid)
    # for x in fakes:
    #     DBWriter.put_chat(fake_room_uuid, x.commit())

    app.run(port=3333)