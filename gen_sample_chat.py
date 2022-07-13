from faker import Faker
import uuid
import random
import datetime
from datetime import timedelta, tzinfo
from chat_type import Chat_Data

# uuid1 -> time based
# uuid4 -> random

fake = Faker('ko-KR')

class TZ_ko(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=9)
    def dst(self, dt):
        return timedelta(0)
    def tzname(self, dt):
        return "+09:00"
    def __repr__(self):
        return f"{self.__class__.__name__}()"

def gen_chat(members : int, count : int, room_uuid : str = None):

    items = []

    ## faking room UUID
    assert room_uuid is None or len(room_uuid) == 36
    ROOM_UUID = room_uuid or str(uuid.uuid4())

    ## faking TIME
    TIME_EXTENtion = 5
    
    basetime = datetime.datetime.now(tz=TZ_ko()).replace(microsecond=0)
    basetime -= datetime.timedelta(seconds=count * TIME_EXTENtion)

    timespan = [1 for _ in range(count)]

    for _ in range(TIME_EXTENtion-1):
        idice = random.choices([i for i in range(count)], k=count)
        for idx in idice:
            timespan[idx] += 1
    assert count * TIME_EXTENtion == sum(timespan)

    faked_TIME = []
    for sec in timespan:
        faked_TIME.append(basetime)
        basetime += timedelta(seconds=sec)
    
    ## faking NAME
    faked_NAME = [fake.name() for _ in range(members)]

    ## faking chats
    for f_time in faked_TIME:
        f_name = random.choice(faked_NAME)
        f_chat = fake.catch_phrase()    # .text(), .paragraph() 사용 가능(영어)
        f_member_uuid = str(uuid.uuid5(uuid.NAMESPACE_OID, f_name))
        f_time_formated =f_time.strftime('%Y-%m-%d %H:%M:%S')

        items.append(Chat_Data (
            None, f_time_formated, f_name, f_member_uuid, f_chat,1 ,1 
        ))
    return items, ROOM_UUID
