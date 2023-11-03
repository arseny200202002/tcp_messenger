from db_model import *

if __name__ == "__main__":
    with db:
        db.create_tables([Users, Sessions, Chats, Messages, ChatsUsers, ChatsMessages])
