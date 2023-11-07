import unittest

import os 
import sys 
cwd = os.getcwd() 
sys.path.append(cwd)

from source.server.server_logic import *

class TestServerLogic(unittest.TestCase):
    def test_responce_parser(self):
        self.assertEqual(parse_responce('COMMAND:BACK'), ('COMMAND', 'BACK'))
        self.assertEqual(parse_responce('COMMAND:EXIT'), ('COMMAND', 'EXIT'))
        self.assertEqual(parse_responce('COMMAND:LOGIN'), ('COMMAND', 'LOGIN'))
        self.assertEqual(parse_responce('DATA:data_1|data_2|data_3'), ('DATA', ['data_1', 'data_2', 'data_3']))
        self.assertEqual(parse_responce('DATA:'), ('DATA', ['']))
        self.assertEqual(parse_responce('ERROR:'), ('ERROR'))
    def test_prosess_responce(self):
        # setup
        test_address = '127.0.0.0'
        test_port = 5002
        update_session(2, datetime.now(), test_address, test_port)

        responce = parse_responce('COMMAND:BACK')
        self.assertEqual(process_responce(test_address, test_port, 1, responce), (0, 'TEMPLATE:authorization'))
        responce = parse_responce('COMMAND:LOGIN')
        self.assertEqual(process_responce(test_address, test_port, 0, responce), (1, 'TEMPLATE:login'))
        responce = parse_responce('DATA:test_login_3|password')
        self.assertEqual(process_responce(test_address, test_port, 1, responce), (3, 'TEMPLATE:main_menu:DATA:test_chat'))
        responce = parse_responce('DATA:test_chat')
        print(process_responce(test_address, test_port, 3, responce))
        responce = parse_responce('COMMAND:BACK')
        print(process_responce(test_address, test_port, 5, responce))
        responce = parse_responce('COMMAND:BACK')
        print(process_responce(test_address, test_port, 3, responce))
        responce = parse_responce('COMMAND:BACK')
        print(process_responce(test_address, test_port, 0, responce))
        responce = parse_responce('COMMAND:EXIT')
        print(process_responce(test_address, test_port, 0, responce))


if __name__ == "__main__":
    #unittest.main()
    test = TestServerLogic().test_prosess_responce()