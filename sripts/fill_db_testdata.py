from collections import namedtuple
from datetime import datetime

import os 
import sys 
cwd = os.getcwd() 
sys.path.append(cwd)

from source.server.db.db_requests import *

user_fields =           [Users.username, Users.password_hash, Users.id]
chat_fields =           [Chats.creator_id, Chats.name, Chats.id]
message_fields =        [Messages.text, Messages.send_date, Messages.author_name, Messages.id]
session_fields =        [Sessions.user_id, Sessions.last_update_time, Sessions.state, Sessions.address, Sessions.port]
chat_message_fields =   [ChatsMessages.chat_id, ChatsMessages.message_id]
chat_user_fields =      [ChatsUsers.chat_id, ChatsUsers.user_id]

now = datetime.now()

users_data = [
    ('name_1', 'password', 1001),
    ('name_2', 'password', 1002),
    ('name_3', 'password', 1003),
    ('name_4', 'password', 1004),
    ]
chats_data = [
    (1001,  'test_chat', 1001),
    (1001,  'test_chat', 1002),
    (1001,  'test_chat', 1003),
    ]
messages_data = [
    ('message_1', now, 'test_name_1', 1001),
    ('message_2', now, 'test_name_2', 1002),
    ('message_3', now, 'test_name_3', 1003),
    ('message_4', now, 'test_name_4', 1004),
    ]
sessions_data = [
    (1001, now, 0, '127.0.0.0', 5001, False),
    (1002, now, 0, '127.0.0.0', 5002, False),
    (1003, now, 0, '127.0.0.0', 5003, False),
    (1004, now, 0, '127.0.0.0', 5004, False),
    ]
chats_messages_data = [
    (1001, 1001),
    (1001, 1002),
    (1001, 1003),
    (1001, 1004),
    ]
chats_users_data = [
    (1001, 1001),
    (1001, 1002),
    (1002, 1001),
    (1002, 1003),
    (1003, 1001),
    (1003, 1004)
    ]

def insert_many(data, table, insert_fields):
    with db.atomic():
        table.insert_many(data, fields=insert_fields).on_conflict_ignore().execute()


if __name__ == "__main__":
    insert_many(users_data,         Users, user_fields)
    insert_many(chats_data,         Chats, chat_fields)
    insert_many(messages_data,      Messages, message_fields)
    insert_many(sessions_data,      Sessions, session_fields)
    insert_many(chats_messages_data,ChatsMessages, chat_message_fields)
    insert_many(chats_users_data,   ChatsUsers, chat_user_fields)
