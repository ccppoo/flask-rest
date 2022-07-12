import pymysql
import json
from pprint import pprint
import os
from dotenv import load_dotenv
from db_query_string import *

load_dotenv()

DB_HOST = os.environ.get('db_host')
DB_USER = os.environ.get('user')
DB_USER_PASSWORD = os.environ.get('password')
DB_NAME = os.environ.get('db_name')

def get_chat_schema():
    with open('./chat_db_schema.json', mode='r') as fp:
        json_obj = json.load(fp)
        return json_obj

def make_chat_table_schema(room_id):
    chat_schema = get_chat_schema()['chat']
    
    a = ',\n'.join([f"{k} {i}" for k, i in chat_schema.items()])

    return making_table.format(room_id, a)

# make_chat_table_schema('chat-1234')
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

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DBWiterHandler, cls).__new__(cls)
        else:
            print('recycle')
        return cls.instance

    @classmethod
    def execute(cls, query : str):
        # FIXME : 나중에 동기화 문제로 인해서 DB connection을 따로 만들것
        cls.cursor.execute(query)
        cls.db.commit()
        return cls.cursor.fetchall()

    @classmethod
    def make_chat_table(cls, room_id):
        a  = make_chat_table_schema(room_id)
        DBWiterHandler.execute(a)

    @classmethod
    def put_chat(cls, room_id, items):
        # print(f"{room_id=}")

        assert list(get_chat_schema()['chat'].keys()) == ['chat_id'] + list(items.keys())

        ii = ', '.join([f'"{x}"' if isinstance(x, str) else f'{x}' for x in items.values()])

        aa = put_chat.format(table_name=room_id, values=ii)
        aaa=DBWiterHandler.execute(aa)

    @classmethod
    def get_chat(cls, room_id, count : int):
        
        aa = get_chat.format(room_id=room_id, count=count)
        a = DBWiterHandler.execute(aa)
        pprint(a)


a = DBWiterHandler()

a.make_chat_table('022db29c-d0e2-11e5-bb4c-60f81dca7676'.replace('-', '_'))
# a.put_chat('chat1234', chat_sample)
a.get_chat('chat1234', 30)
