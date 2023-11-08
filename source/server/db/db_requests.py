from .db_model import *
from datetime import datetime

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
            return False # если при транзакции возникли ошибки или исключения то вернется None
    return inner

# create requests

@exception_handler
def create_session(time: datetime, address: str, port: int):
    session = Sessions(last_update_time=time, address=address, port=port, state=0)
    session.save(force_insert=True)

@exception_handler
def create_user(username:str, password: str, address: str, port: int) -> int:
    user = Users(username=username, password_hash=password)
    user.save(force_insert=True)
    now = datetime.now()
    user_id = get_user_id(username)
    connect_session(user_id, now, address, port) 
    return user.id

@exception_handler
def create_chat(creator_id: int, name: str, user_1_id: int, user_2_id: int):
    chat = Chats(creator_id=creator_id, name=name)

    chat.save(force_insert=True)
    chat_user_2 = ChatsUsers(chat_id=chat.id, user_id=user_1_id).save(force_insert=True)
    chat_user_3 = ChatsUsers(chat_id=chat.id, user_id=user_2_id).save(force_insert=True)

@exception_handler        
def create_message(chat_id: int, text: str, send_date: str, author_name: str):
    message = Messages(text=text, send_date=send_date, author_name=author_name)

    message.save(force_insert=True)
    chat_message = ChatsMessages(chat_id=chat_id, message_id=message.id).save(force_insert=True)

# get requests
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

# if there is no such row in db -> return None
def get_user_id(username: str) -> int:
    query = Users.select(Users.id).where(Users.username == username)
    if len(query) == 0:
        return None
    return query[0].id

def get_user_id_by_session(address: str, port: int) -> int:
    query = Sessions.select(Sessions.user_id).where(Sessions.address == address, Sessions.port == port)
    if len(query) == 0:
        return None
    return query[0].user_id

def get_chat_id(chat_name: str) -> int:
    query = Chats.select(Chats.id).where(Chats.name == chat_name)
    if len(query) == 0:
        return None
    return query[0].id

def get_state(address: str, port: int) -> int:
    query = Sessions.select(Sessions.state).where(Sessions.address == address, Sessions.port == port)
    if len(query) == 0:
        return None
    else:
        return query[0].state

def get_current_chat(address: str, port: int) -> int:
    query = (Sessions
             .select(Sessions.chat_id)
             .join(Users, on=(Users.id == Sessions.user_id))
             .where(Sessions.address == address, Sessions.port == port))
    if len(query) == 0:
        return None
    else:
        return query[0].chat_id

def get_username(address: str, port: int) -> str:
    query = (Users
             .select(Users.username)
             .join(Sessions, on=(Users.id == Sessions.user_id))
             .where(Sessions.address == address, Sessions.port == port))
    if len(query) == 0:
        return None
    else:
        return query[0].username

# other requests

@check_requests
def check_user_existence(username: str, password: str):
    query = Users.select().where(Users.username == username, Users.password_hash == password)
    return query

@exception_handler
def connect_session(user_id: int, time: datetime, address: str, port: int):
    query = (Sessions
             .update(user_id=user_id, last_update_time=time)
             .where(Sessions.address == address, Sessions.port == port))
    query.execute()

@exception_handler
def set_chat(chat_id: int, time: datetime, address: str, port: int):
    query = (Sessions
             .update(chat_id=chat_id, last_update_time=time)
             .where(Sessions.address == address, Sessions.port == port))
    query.execute()

@exception_handler
def update_session(state: int, time: datetime, address: str, port: int, chat_id: int = None):
    query = (Sessions
             .update(state=state, last_update_time=time)
             .where(Sessions.address == address, Sessions.port == port))
    query.execute()

# TO DO
def end_old_sessions():
    pass