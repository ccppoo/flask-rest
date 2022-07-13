making_table = """
CREATE TABLE IF NOT EXISTS {} (
        {}
)
"""

put_chat = """
INSERT INTO {table_name}
VALUES (NULL, {values});
"""

get_chat = """
SELECT chat_id, created_at, member_nickname, member_uuid, chat_content, media_type, message_state
FROM chat_db.{room_id}
ORDER BY chat_id DESC
LIMIT {count};
"""

get_chat_tables = """
SELECT 
	TABLE_NAME
FROM INFORMATION_SCHEMA.tables
WHEre TABLE_SCHEMA = 'chat_db'
ORDER BY  UPDATE_TIME
"""
# TABLE_NAME, TABLE_ROWS, CREATE_TIME, UPDATE_TIME
