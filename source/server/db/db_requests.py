#from .db_model import *
from .db_model import *

def check_requests(func):
    def inner(*args, **kwargs):
        query = func(*args, **kwargs)

        if query.exists(): return True
        else: return False
    return inner

@check_requests
def check_sing_in(login_: str, password_hash_: str):
    query = Users.select().where(Users.login == login_, Users.password_hash == password_hash_)
    return query

@check_requests
def check_sing_up(login_: str):
    query = Users.select().where(Users.login == login_)
    return query

def create_user(username_: str, password_hash_: str, login_: str, mail_: str=None):
    query = Users.insert(username=username_,
                         password_hash=password_hash_,
                         login=login_,
                         mail=mail_)
    try:
        user_id = query.execute()
        return user_id
    except Exception as e:
        return Exception

def get_user_id(username_: str) -> int:
    user_id = Users.select(Users.id).where(Users.username == username_).get()
    return user_id

def create_chat(user_1_id: int, user_2_id: int, creator_id_: int, chat_name_: str=None):
    query = Chats.insert(creator_id=creator_id_,
                         name=chat_name_)
    chat_id_ = query.execute()

    query_1 = ChatsUsers.insert(chat_id=chat_id_,
                                user_id=user_1_id)
    query_2 = ChatsUsers.insert(chat_id=chat_id_,
                                user_id=user_2_id)
    
    try:
        query_1.execute()
        query_2.execute()
        return True
    except:
        return False
    
