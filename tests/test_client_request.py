import unittest

import os 
import sys 
cwd = os.getcwd() 
sys.path.append(cwd)

from source.client.client_logic import *

def input_validation(input, len_of_data=1):
    if len(input) == 0: return 'error'
    if input in commands.values() or input in basic_commands.values():
        return requests.command_request(input)
    words = re.findall(r'\b\S+\b', input)
    if len(words) != len_of_data: return 'error'
    return requests.data_request(words)

class TestClientRequests(unittest.TestCase):
    def test_input_validation_func(self):
        self.assertEqual(input_validation(''), 'error')
        self.assertEqual(input_validation('LOGIN'), b'COMMAND:LOGIN')
        self.assertEqual(input_validation('BACK'), b'COMMAND:BACK')
        self.assertEqual(input_validation('EXIT'), b'COMMAND:EXIT')
        self.assertEqual(input_validation('test_login test_password', 2), b'DATA:test_login|test_password|')
        self.assertEqual(input_validation('test_login test_password', 3), 'error')

    def test_parse_answer(self):
        self.assertEqual(parse_server_answer('TEMPLATE:start').template, 'start')
        self.assertEqual(parse_server_answer('TEMPLATE:sing_in:DATA:test_1:test_2'), server_answer('sing_in', ['test_1', 'test_2']))
        self.assertEqual(parse_server_answer('ERROR').template, 'error')

if __name__ == "__main__":
    unittest.main()
