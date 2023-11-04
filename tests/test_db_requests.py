import unittest

import os 
import sys 
cwd = os.getcwd() 
sys.path.append(cwd)

from source.server.db.db_requests import *


class TestDbRequests(unittest.TestCase):
    
    def test_check_sing_in(self):
        self.assertEqual(check_sing_in('test_login', 'test_password'), True)
        self.assertEqual(check_sing_in('dont_exist', 'test_password'), False)


if __name__ == "__main__":
    unittest.main()
    