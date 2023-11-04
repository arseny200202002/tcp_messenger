import unittest
from datetime import datetime

import os 
import sys 
cwd = os.getcwd() 
sys.path.append(cwd)

from source.server.db.db_requests import *

""" test configuration:
users:
    exists:
        id: 1 'test_login' 'test_password' 'test_login'
        id: 2 'test_insert' 'test_password' 'test_insert'
    do not exist:
        'dont_exist' 'test_password' 'dont_exist' 
"""

class TestDbRequests(unittest.TestCase):
    
    def test_check_sing_in(self):
        self.assertEqual(check_sing_in('test_login', 'test_password'), True)
        self.assertEqual(check_sing_in('dont_exist', 'test_password'), False)

    def test_check_sing_up(self):
        self.assertEqual(check_sing_up('test_login'), True)
        self.assertEqual(check_sing_up('dont_exist'), False)
    
    def test_create_user(self):
        self.assertEqual(create_user('test_login', 'test_password', 'test_login'), Exception)
        time = datetime.now().time()
        self.assertEqual(type(create_user(f'{time}', 'test_password', f'{time}')), int)

    def test_create_chat(self):
        self.assertEqual(create_chat(1, 2, 1, 'test_chat'), True)


if __name__ == "__main__":
    unittest.main()
    