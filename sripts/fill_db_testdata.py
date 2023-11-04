from collections import namedtuple
from datetime import datetime

import os 
import sys 
cwd = os.getcwd() 
sys.path.append(cwd)

from source.server.db.db_requests import *

user = namedtuple('user', ['username', 'password_hash', 'login', 'id', 'mail'])

User_1 = user('test_name_1', 'password', 'test_login_1', 1001, None)
User_2 = user('test_name_2', 'password', 'test_login_2', 1002, None)
User_3 = user('test_name_3', 'password', 'test_login_3', 1003, None)
User_4 = user('test_name_4', 'password', 'test_login_4', 1004, None)

if __name__ == "__main__":
    # Users
    create_user(*User_1)
    create_user(*User_2)
    create_user(*User_3)
    create_user(*User_4)
    #Chats
    create_chat(1001, 1002, 1001, 'test_chat', 1000)
    create_chat(1001, 1003, 1001, 'test_chat', 1001)
    #Messages
    now = datetime.now()
    create_message(1001, 'message_1', now, 'test_name_1')
    create_message(1001, 'message_2', now, 'test_name_1')
    create_message(1001, 'message_3', now, 'test_name_1')
