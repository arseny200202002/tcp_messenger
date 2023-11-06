from .db_model import *
from datetime import datetime
import random

def check_requests(func):
    def inner(*args, **kwargs):
        query = func(*args, **kwargs)

        if query.exists(): return True
        else: return False
    return inner

# при отладке нужно убрать комментарий
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

@exception_handler
def create_session(session: Sessions):
    #session = Sessions()
    session.save(force_insert=True)

@exception_handler
def create_user(user: Users, address: str, port: int):
    user.save(force_insert=True)
    now = datetime.now()
    update_session(4, now, address, port) # state 4 stands fro main menu
    return user.id

@exception_handler
def create_chat(chat: Chats, user_1_id: int, user_2_id: int):
    chat.save(force_insert=True)
    chat_id_ = chat.id

    chat_user_2 = ChatsUsers(chat_id=chat_id_, user_id=user_1_id).save(force_insert=True)
    chat_user_3 = ChatsUsers(chat_id=chat_id_, user_id=user_2_id).save(force_insert=True)

@exception_handler        
def create_message(chat_id: int, message: Messages):
    message.save(force_insert=True)
    chat_message = ChatsMessages(chat_id=chat_id, message_id=message.id).save(force_insert=True)

def get_message_history(chat_id: int) -> list:
    query = (Messages
             .select(Messages.text, Messages.send_date, Messages.author_name)
             .join(ChatsMessages, on=(Messages.id == ChatsMessages.message_id))
             .where(ChatsMessages.chat_id == chat_id))
    messages = [[message.text, message.send_date, message.author_name] for message in query]
    return messages                    

def get_chats(user_id: int) -> list:
    query = (Chats
             .select(Chats.name)
             .join(ChatsUsers, on=(Chats.id == ChatsUsers.chat_id))
             .where(ChatsUsers.user_id == user_id))
    chats = [chat.name for chat in query]
    return chats

def get_user_id(login: str) -> int:
    user_id = Users.get(Users.login == login).id
    return user_id

def get_state(address: IPField):
    state = Sessions.get(Sessions.address == address).state
    return state

@exception_handler
def update_session(state: int, time: datetime, address: str, port: int):
    query = Sessions.update(state=state, last_update_time=time).where(Sessions.address == address, Sessions.port == port)
    query.execute()