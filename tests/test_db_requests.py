import unittest
from datetime import datetime

import os 
import sys 
cwd = os.getcwd() 
sys.path.append(cwd)

from source.server.db.db_requests import *

class TestDbRequests(unittest.TestCase):
    
    def test_check_sing_in(self):
        self.assertEqual(check_sing_in('test_login_1', 'password'), True)
        self.assertEqual(check_sing_in('dont_exist', 'password'), False)

    def test_check_sing_up(self):
        self.assertEqual(check_sing_up('test_login_1'), True)
        self.assertEqual(check_sing_up('dont_exist'), False)
    
    def test_create_user(self):
        self.assertEqual(create_user('test_name_1', 'password', 'test_login_1'), Exception)
        time = datetime.now().time()
        self.assertEqual(type(create_user(f'{time}', 'test_password', f'{time}')), int)

    def test_create_chat(self):
        self.assertEqual(create_chat(1001, 1002, 1001, 'test_chat'), True)

    def test_create_message(self):
        now = datetime.now()
        self.assertEqual(create_message(1001, str(now), now, 'test_login_1'), True)


if __name__ == "__main__":
    unittest.main()
    