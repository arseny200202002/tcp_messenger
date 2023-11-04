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

# настроить передачу параметров в виде кортежа для его распаковки
def create_user(username_: str, password_hash_: str, login_: str, id_: int=None, mail_: str=None):
    query = Users.insert(username=username_,
                         password_hash=password_hash_,
                         login=login_,
                         mail=mail_,
                         id=id_)
    try:
        user_id = query.execute()
        return user_id
    except Exception as e:
        return Exception

def get_user_id(username_: str) -> int:
    user_id = Users.select(Users.id).where(Users.username == username_).get()
    return user_id

def create_chat(user_1_id: int, user_2_id: int, creator_id_: int, chat_name_: str=None, id_: int=None):
    query_1 = Chats.insert(creator_id=creator_id_,
                           name=chat_name_,
                           id=id_)
    chat_id_ = query_1.execute()

    query_2 = ChatsUsers.insert(chat_id=chat_id_,
                                user_id=user_1_id)
    query_3 = ChatsUsers.insert(chat_id=chat_id_,
                                user_id=user_2_id)
    
    try:
        query_2.execute()
        query_3.execute()
        return True
    except:
        return False
    
def create_message(chat_id_: int, message_text: str, send_date_, author: str):
    query_1 = Messages.insert(text=message_text,
                              send_date=send_date_,
                              author_name=author)
    
    message_id_ = query_1.execute()

    query_2 = ChatsMessages.insert(chat_id=chat_id_,
                                   message_id=message_id_)

    query_2.execute()



