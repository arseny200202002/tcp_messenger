from peewee import *
import configparser
from .db_config import DB

"""
config = configparser.ConfigParser()
config.read('source\db\db_config.ini')
db_settings = config['db']
name = db_settings['NAME']
user = db_settings['USER']
password = db_settings['PASSWORD']
host = db_settings['HOST']
port = db_settings['PORT']
"""

db = PostgresqlDatabase(
    DB.NAME,
    user=DB.USER,
    password=DB.PASSWORD,
    host=DB.HOST,
    port=DB.port
    )

class BaseModel(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db
        order = 'id'

class Users(BaseModel):
    username =      CharField(null=False, unique=True)
    password_hash = CharField(null=False)

    class Meta:
        db_table = 'Users'

class Sessions(BaseModel):
    user_id =           IntegerField(null=True)
    last_update_time =  DateTimeField()
    state =             IntegerField(default=0)
    address =           IPField(null=False)
    port =              IntegerField(null=False)
    chat_id =           IntegerField(null=True)

    class Meta:
        db_table = 'Sessions'
        primary_key = CompositeKey('address', 'port')

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
    text =          TextField(null=False)
    send_date =     DateTimeField()
    author_name =   CharField(null=False)

    class Meta:
        db_table = 'Messages'

class ChatsMessages(BaseModel):
    chat_id =       ForeignKeyField(Chats)
    message_id =    ForeignKeyField(Messages)

    class Meta:
        db_table = 'ChatsMessages'
