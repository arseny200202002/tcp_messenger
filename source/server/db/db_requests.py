from db_model import *

def check_sing_in(login_, password_hash_):
    query = Users.select(1).where(Users.login == login_, Users.password_hash == password_hash_)
    query.execute()
    print(query)

def check_sing_up(login_):
    query = Users.select(1).where(Users.login == login_)
    query.execute()
    print(query)

def create_user(username_, password_hash_, login_, mail_=None):
    query = Users.insert(username=username_,
                         password_hash=password_hash_,
                         login=login_,
                         mail=mail_)
    query.execute()

def create_chat(user_1_id, user_2_id, creator_id, chat_name=None):
    query = Chats.insert()