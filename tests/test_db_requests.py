import unittest
from datetime import datetime
import ipaddress
import random


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

class TestCreateRequests(unittest.TestCase):  
    def test_create_user(self):
        address, port = random_addr_port()
        self.assertEqual(create_user('name_1', 'password', address, port), False)
        # setup 
        time = datetime.now()
        address, port = random_addr_port()
        create_session(time, address, port)

        self.assertEqual(type(create_user(f'{time}', 'password', address, port)), int)

    def test_create_session(self):
        address, port = random_addr_port()
        create_session(datetime.now(), address, port)
        self.assertEqual(session_existence(state=0, address=address, port=port), True)
    
    def test_create_chat(self):
        create_chat(creator_id=1001, name='test_chat', user_1_id=1001, user_2_id=1002) 
        self.assertEqual(create_chat(creator_id=10000, name='test_chat', user_1_id=10000, user_2_id=10000), False) 
        self.assertEqual(chat_existence(1001, 'test_chat'), True)

    def test_create_message(self):
        now = datetime.now()
        create_message(chat_id=1002, text=str(now), send_date=now, author_name=str(now))
        self.assertEqual(message_existence(str(now), str(now)), True)

class TestGetRequests(unittest.TestCase):
    def test_get_message_history(self):
        self.assertEqual(len(get_message_history(1001)), 4)
        self.assertEqual(len(get_message_history(10000)), 0)

    def test_get_chats(self):
        self.assertEqual(len(get_chats(1003)), 1)
        self.assertEqual(len(get_chats(10000)), 0)

    def test_get_user_id(self):
        self.assertEqual(get_user_id('name_1'), 1001)
        self.assertEqual(get_user_id('dont_exists'), None)
    
    def test_get_chat_id(self):
        self.assertEqual(get_chat_id('test_chat'), 1001)
        self.assertEqual(get_chat_id('no_such_chat'), None)

    def test_get_state(self):
        self.assertEqual(get_state(integer_to_ip(2130706432), 5002), 0)
        self.assertEqual(get_state(integer_to_ip(0), 5002), None)
    
    def test_get_user_id_by_session(self):
        self.assertEqual(get_user_id_by_session(integer_to_ip(2130706432), 5001), 1001)
        self.assertEqual(get_user_id_by_session(integer_to_ip(2130706432), 0), None)

    def test_get_current_chat(self):
        #self.assertEqual(get_current_chat(integer_to_ip(2130706432), 5001), )
        self.assertEqual(get_current_chat(integer_to_ip(2130706432), 5001), None)

    def test_get_username(self):
        self.assertEqual(get_username(integer_to_ip(2130706432), 5001), 'name_1')

class OtherRequests(unittest.TestCase):
    def test_check_sing_in(self):
        self.assertEqual(check_user_existence('name_1', 'password'), True)
        self.assertEqual(check_user_existence('dont_exist', 'password'), False)

    def test_update_session(self):
        now = datetime.now()
        update_session(1000, now, '127.0.0.0', 5001)
        self.assertEqual(session_existence(state=1000, address='127.0.0.0', port=5001), True)

    def test_connect_session(self):
        address, port = random_addr_port()
        create_session(datetime.now(), address, port)
        connect_session(1001, datetime.now(), address, port)
        self.assertEqual(get_user_id_by_session(address, port), 1001)

    def test_set_chat(self):
        set_chat(10000, datetime.now(), integer_to_ip(2130706432), 5002)
        self.assertEqual(get_current_chat(integer_to_ip(2130706432), 5002), 10000)

if __name__ == "__main__":
    unittest.main()
    #create_tests = TestCreateRequests().test_create_chat()
    