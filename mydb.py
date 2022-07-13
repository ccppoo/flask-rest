import pymysql
import json
from pprint import pprint
import os
from dotenv import load_dotenv
from db_query_string import *
import uuid
from chat_type import Chat_Data
from itertools import chain

# __all__ = [

# ]

load_dotenv()

DB_HOST = os.environ.get('db_host')
DB_USER = os.environ.get('user')
DB_USER_PASSWORD = os.environ.get('password')
DB_NAME = os.environ.get('db_name')

def __get_chat_schema():
    with open('./chat_db_schema.json', mode='r') as fp:
        json_obj = json.load(fp)
        return json_obj


CHAT_SCHEMA: json = __get_chat_schema()

def _make_chat_table_query(room_id):
    chat_schema = CHAT_SCHEMA['chat']
    
    a = ',\n'.join([f"{k} {i}" for k, i in chat_schema.items()])

    return making_table.format(room_id, a)


'''
Only Write
'''
class DBWiterHandler(object):

    db = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_USER_PASSWORD,
        db=DB_NAME,
        charset='utf8')
    cursor = db.cursor()

    ROOMS = []

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DBWiterHandler, cls).__new__(cls)
        else:
            print('recycle')
        return cls.instance

    ### limit direct access ###

    @classmethod
    def _execute(cls, query : str):
        # FIXME : 나중에 동기화 문제로 인해서 DB connection을 따로 만들것
        cls.cursor.execute(query)
        cls.db.commit()
        return cls.cursor.fetchall()

    @classmethod
    def _make_chat_table(cls, room_id):
        room_id = room_id.replace('-', '_')
        a = _make_chat_table_query(room_id)
        DBWiterHandler._execute(a)

    ### allow direct access ###

    @classmethod
    def make_new_room(cls, room_name):

        room_id = uuid.uuid5(uuid.NAMESPACE_OID, room_name)
        room_id = room_id.replace('-', '_')
        DBWiterHandler._make_chat_table(room_id)
        return room_id

    @classmethod
    def get_room_list(cls,):
        a=  DBWiterHandler._execute(get_chat_tables)
        b =  list(chain(*[aa for aa in a]))
        return b

    '''
    나중에 읽기 쓰기 따로하는 DB 매니저 만들기
    '''
    @classmethod
    def put_chat(cls, room_id, items):
        room_id = room_id.replace('-', '_')

        # pprint(list(CHAT_SCHEMA['chat'].keys()))
        # pprint(list(items.keys()))
        assert list(CHAT_SCHEMA['chat'].keys()) == [
            'chat_id'] + list(items.keys())

        ii = ', '.join([f'"{x}"' if isinstance(x, str) else f'{x}' for x in items.values()])

        aa = put_chat.format(table_name=room_id, values=ii)
        aaa = cls._execute(aa)

    @classmethod
    def get_chat(cls, room_id, count : int):
        room_id = room_id.replace('-', '_')
        aa = get_chat.format(room_id=room_id, count=count)
        a = cls._execute(aa)

        chat_data = []
        for line in a:
            chat_data.append(Chat_Data(*line))
        
        # pprint(chat_data)
        return chat_data

if __name__ == "__main__":

    pass
    # a = DBWiterHandler()
    # a._make_chat_table('022db29c-d0e2-11e5-bb4c-60f81dca7676'.replace('-', '_'))
    # a.get_chat('chat1234', 30)