from .db_model import *

def check_requests(func):
    def inner(*args, **kwargs):
        query = func(*args, **kwargs)

        if query.exists(): return True
        else: return False
    return inner

@check_requests
def check_sing_in(login_, password_hash_):
    query = Users.select().where(Users.login == login_, Users.password_hash == password_hash_)
    return query

@check_requests
def check_sing_up(login_):
    query = Users.select().where(Users.login == login_)
    return query

def create_user(username_, password_hash_, login_, mail_=None):
    query = Users.insert(username=username_,
                         password_hash=password_hash_,
                         login=login_,
                         mail=mail_)
    try:
        query.execute()
    except Exception as e:
        print(Exception)

def get_user_id(username_) -> int:
    user_id = Users.select(Users.id).where(Users.username == username_).get()
    return user_id

def create_chat(user_1_id, user_2_id, creator_id_, chat_name_=None):
    query = Chats.insert(creator_id=creator_id_,
                         chat_name=chat_name_)
    chat_id_ = query.execute()

    query_1 = ChatsUsers.insert(chat_id=chat_id_,
                                user_id=user_1_id)
    query_2 = ChatsUsers.insert(chat_id=chat_id_,
                                user_id=user_1_id)
    
    query_1.execute()
    query_2.execute()
    


if __name__ == "__main__":
    # check_sing_in('test_login', 'test_password')
    # check_sing_in('test_login_2', 'test_password')
    #create_user('test_insert_2', 'test_password', 'test_insert_2')
    create_user('test_login_2', 'test_password', 'test_login_2')
