from dataclasses import dataclass, asdict


@dataclass
class Chat_Data:
    chat_id : int
    created_at : str
    member_nickname : str
    member_uuid : str
    chat_content : str
    media_type : int
    message_state : int

    # def export_json(self, ):
    #     return 

    def commit(self, ):
        temp = asdict(self)
        temp.pop('chat_id')
        return temp


#필요한거
['chat_id',
 'room_uuid',
 'created_at',
 'member_nickname',
 'member_uuid',
 'chat_content',
 'media_type',
 'message_state']

['created_at',
 'member_nickname',
 'member_uuid',
 'chat_content',
 'media_type',
 'message_state']
