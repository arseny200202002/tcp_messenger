from .db_model import *

def check_requests(func):
    def inner(*args, **kwargs):
        query = func(*args, **kwargs)

        if query.exists(): return True
        else: return False
    return inner

def exception_handler(func):
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            #print(f"An exception occured: {str(e)}")
            return Exception
    return inner

@check_requests
def check_sing_in(login_: str, password_hash_: str):
    query = Users.select().where(Users.login == login_, Users.password_hash == password_hash_)
    return query

@check_requests
def check_sing_up(login_: str):
    query = Users.select().where(Users.login == login_)
    return query

def get_user_id(login_: str) -> int:
    user_id = Users.get(Users.login == login_).id
    return user_id

@exception_handler
def create_user(user: Users):
    user.save(force_insert=True)
    return user.id

@exception_handler
def create_chat(chat: Chats, user_1_id: int, user_2_id: int):
    chat.save(force_insert=True)
    chat_id_ = chat.id

    chat_user_2 = ChatsUsers(chat_id=chat_id_, user_id=user_1_id).save(force_insert=True)
    chat_user_3 = ChatsUsers(chat_id=chat_id_, user_id=user_2_id).save(force_insert=True)

@exception_handler        
def create_message(chat_id_: int, message: Messages):
    message.save(force_insert=True)
    chat_message = ChatsMessages(chat_id=chat_id_, message_id=message.id).save(force_insert=True)
