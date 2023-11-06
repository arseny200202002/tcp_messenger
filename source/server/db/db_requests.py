from .db_model import *
from datetime import datetime

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
    now = datetime.now()
    session.last_update_time = now
    session.save(force_insert=True)

@exception_handler
def create_user(user: Users):
    user.save(force_insert=True)
    now = datetime.now()
    session = Sessions(user_id=user.id, last_update_date=now, state=-1, is_guest=False)
    create_session(session)
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

@exception_handler
def update_session(user_id: int, state: int, time: datetime):
    query = Sessions.update(state=state, last_update_time=time).where(Sessions.user_id == user_id)
    query.execute()