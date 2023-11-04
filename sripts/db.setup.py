import os 
import sys 
cwd = os.getcwd() 
sys.path.append(cwd)

from source.server.db.db_model import *

tables = [Users, Sessions, Chats, Messages, ChatsUsers, ChatsMessages]

def delete_tables():
    with db:
        db.drop_tables(tables)

def create_tables():
    with db:
        db.create_tables(tables)

if __name__ == "__main__":
    delete_tables()
    create_tables()





    
    
