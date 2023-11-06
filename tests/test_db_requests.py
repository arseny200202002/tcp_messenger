import unittest
from datetime import datetime
import ipaddress

import os 
import sys 
cwd = os.getcwd() 
sys.path.append(cwd)

from source.server.db.db_requests import *

def integer_to_ip(address: int) -> str:
    """
    receives: ip address in integer format \n
    returns: ip address in string format
    """
    return ipaddress.ip_address(address).__str__()

def random_addr_port() -> tuple:
    """
    returns: tuple: address, port \n
    of random address out of (0, 100000) \n
    and random port out of range (0, 10000)
    """
    address = integer_to_ip(random.randrange(0, 100000))
    port = random.randrange(0, 10000)
    return address, port

def session_existence(state:int, address: str, port: int) -> bool:
    query = Sessions.select().where(Sessions.address == address, Sessions.port == port, Sessions.state == state)
    if query.exists():
        return True
    else:
        return False

def chat_existence(creator_id: int, name: str) -> bool:
    chat = Chats.select().where(Chats.creator_id == creator_id, Chats.name == name)
    if chat.exists():
        return True
    else:
        return False

def user_existence(login: str) -> bool:
    user = Users.select().where(Users.login == login)
    if user.exists():
        return True
    else:
        return False
    
def message_existence(text: str, author_name: str):
    message = Messages.select().where(Messages.text == text, Messages.author_name == author_name)
    if message.exists():
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
        address, port = random_addr_port()
        self.assertEqual(create_user('test_login_1', 'password', 'test_name_1', address, port), Exception)

        time = datetime.now()
        address, port = random_addr_port()

        self.assertEqual(type(create_user(f'{time}', 'password', f'{time}', address, port)), int)

    def test_create_chat(self):
        create_chat(1001, 'test_chat', 1001, 1002)
        self.assertEqual(chat_existence(1001, 'test_chat'), True)

    def test_create_message(self):
        now = datetime.now()
        create_message(1002, str(now), now, str(now))
        self.assertEqual(message_existence(str(now), str(now)), True)

    def test_create_session(self):
        # setup test data
        now = datetime.now()
        address, port = random_addr_port()

        create_session(now, address, port)
        # check session existence
        self.assertEqual(session_existence(0, address, port), True)
    
    def test_get_message_history(self):
        self.assertEqual(len(get_message_history(1001)), 4)

    def test_get_chats(self):
        self.assertEqual(len(get_chats(1003)), 1)

    def test_update_session(self):
        now = datetime.now()
        update_session(1000, now, '127.0.0.0', 5001)
        self.assertEqual(session_existence(state=1000, address='127.0.0.0', port=5001), True)

    def test_get_state(self):
        self.assertEqual(get_state(integer_to_ip(2130706432), 5002), 0)

if __name__ == "__main__":
    unittest.main()
    #tests = TestDbRequests().test_get_state()
    