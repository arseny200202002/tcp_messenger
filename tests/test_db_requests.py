import unittest
from datetime import datetime

import os 
import sys 
cwd = os.getcwd() 
sys.path.append(cwd)

from source.server.db.db_requests import *

def row_existence(object:BaseModel):
    query = type(object).select().where(type(object).id == object.id)
    if query.exists():
        return True
    else:
        return False

class TestDbRequests(unittest.TestCase):
    
    def test_check_sing_in(self):
        self.assertEqual(check_sing_in('test_login_1', 'password'), True)
        self.assertEqual(check_sing_in('dont_exist', 'password'), False)

    def test_check_sing_up(self):
        self.assertEqual(check_sing_up('test_login_1'), True)
        self.assertEqual(check_sing_up('dont_exist'), False)
    
    def test_get_user_id(self):
        self.assertEqual(get_user_id('test_login_1'), 1001)

    def test_create_user(self):
        user_1 = Users(username='test_name_1', password_hash='password', login='test_login_1')
        self.assertEqual(create_user(user_1), Exception)

        time = datetime.now().time()
        user_2 = Users(username=f'{time}', password_hash='test_password', login=f'{time}')
        self.assertEqual(type(create_user(user_2)), int)

    def test_create_chat(self):
        chat = Chats(creator_id=1001, name='test_chat')
        create_chat(chat, 1001, 1002)
        self.assertEqual(row_existence(chat), True)

    def test_create_message(self):
        now = datetime.now()
        message = Messages(text = str(now), send_date=now, author_name='test_login_1')
        create_message(1001, message)
        self.assertEqual(row_existence(message), True)


if __name__ == "__main__":
    unittest.main()
    