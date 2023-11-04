from peewee import *

from .db_config import DB

db = PostgresqlDatabase(DB.NAME,
                        user=DB.USER,
                        password=DB.PASSWORD,
                        host=DB.HOST,
                        port=DB.port)

class BaseModel(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db
        order = 'id'

class Users(BaseModel):
    username =      CharField(null=False, unique=True)
    password_hash = CharField(null=False)
    login =         CharField(null=False, unique=True)
    mail =          CharField(null=True, default=None, unique=True)

    class Meta:
        db_table = 'Users'

class Sessions(BaseModel):
    user_id =           ForeignKeyField(Users, backref='sessions')
    last_update_time =  DateTimeField()
    state =             IntegerField()

    class Meta:
        db_table = 'Sessions'

class Chats(BaseModel):
    creator_id =    ForeignKeyField(Users)
    name =          CharField(null=True, default=None)

    class Meta:
        db_table = 'Chats'

class ChatsUsers(BaseModel):
    chat_id = ForeignKeyField(Chats)
    user_id = ForeignKeyField(Users, backref='chats')

    class Meta:
        db_table = 'ChatsUsers'

class Messages(BaseModel):
    text =      TextField(null=False)
    send_date = DateTimeField()

    class Meta:
        db_table = 'Messages'

class ChatsMessages(BaseModel):
    chat_id =       ForeignKeyField(Chats)
    message_id =    ForeignKeyField(Messages)

    class Meta:
        db_table = 'ChatsMessages'