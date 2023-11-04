from collections import namedtuple
from datetime import datetime

import os 
import sys 
cwd = os.getcwd() 
sys.path.append(cwd)

from source.server.db.db_requests import *

User_1 = Users(username='test_name_1', password_hash='password', login='test_login_1', id=1001)
User_2 = Users(username='test_name_2', password_hash='password', login='test_login_2', id=1002)
User_3 = Users(username='test_name_3', password_hash='password', login='test_login_3', id=1003)
User_4 = Users(username='test_name_4', password_hash='password', login='test_login_4', id=1004)

chat_1 = Chats(creator_id=1001, name='test_chat', id=1001)
chat_2 = Chats(creator_id=1001, name='test_chat', id=1002)

now = datetime.now()
message_1 = Messages(text='message_1', send_date=now, author_name='test_name_1')
message_2 = Messages(text='message_2', send_date=now, author_name='test_name_2')
message_3 = Messages(text='message_2', send_date=now, author_name='test_name_2')

if __name__ == "__main__":
    # Users
    create_user(User_1)
    create_user(User_2)
    create_user(User_3)
    create_user(User_4)
    #Chats
    create_chat(chat_1, 1001, 1002)
    create_chat(chat_2, 1001, 1003)
    #Messages
    now = datetime.now()
    create_message(1001, message_1)
    create_message(1001, message_2)
    create_message(1001, message_3)
