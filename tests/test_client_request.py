import unittest

import os 
import sys 
cwd = os.getcwd() 
sys.path.append(cwd)

from source.client.client_logic import requests

class TestClientRequests(unittest.TestCase):
    def test_start_request(self):
        pass

if __name__ == "__main__":
    unittest.main()
