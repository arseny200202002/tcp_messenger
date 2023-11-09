from db.db_requests import *
import re
import logging

state_names = {
    0: 'authorization',
    1: 'login',
    2: 'registration',
    3: 'main_menu',
    4: 'chat_creation',
    5: 'in_chat',
}

basic_commands = {
    'EXIT': 'authorization'
    }

state_tree = {
    'authorization':
        {'LOGIN':       'login',
         'REGISTER':    'registration',
         'BACK':        'authorization'},
    'login':
        {'DATA':        'main_menu',
         'BACK':        'authorization'},
    'registration':
        {'DATA':        'main_menu',
         'BACK':        'start'},
    'main_menu': 
        {'CREATE':      'chat_creation',
         'DATA':        'in_chat',
         'BACK':        'start'},
    'chat_creation': 
        {'DATA':        'in_chat',
         'BACK':        'menu'},
    'in_chat':          
        {'DATA':        'in_chat',
         'BACK':        'menu'},
}

class templates:
    def authorization() -> str:
        request = '<text>'
        request += 'для входа введите: LOGIN\n'
        request += 'для регистрации введите: REGISTER'
        request += '<input>'
        return request
    
    def login() -> str:
        request = '<text>'
        request += 'введите имя и пароль'
        request += '<input>'
        return request
    
    def registration() -> str:
        request = '<text>'
        request += 'введите отображаемое имя и пароль'
        request += '<input>'
        request += '<text>'
        request += 'повторите пароль'
        request += '<input>'
        return request
    
    def main_menu() -> str:
        request = '<text>'
        request += 'для создания чата введите: CREATE'
        request += 'чтобы выбрать чат введите его название'
        request += '<input>'
        return request
    
    def chat_creation() -> str:
        request = '<text>'
        request += 'для создания чата введите имя пользователя'
        request += '<input>'
        request += '<text>'
        request += '<input>'
        return request
    
    def in_chat() -> str:
        request = '<text>'
        request += 'введите текст сообщения'
        return request
    
    template = {
        'authorization':    authorization, 
        'login':            login,           
        'registration':     registration,    
        'main_menu':        main_menu,
        'chat_creation':    chat_creation,     
        'in_chat':          in_chat,
    }
    
class state_machine:
    def authorization(address, port):
        pass

    def login(address: str, port: int, username: str, password: str):
        if check_user_existence(username, password):
            user_id = get_user_id(username)
            connect_session(user_id, datetime.now(), address, port)
            chats = get_chats(user_id)
            return chats
        else:
            return False
    
    def registration(address: str, port: int, username: str, password: str):
        if check_user_existence(username, password):
            return False
        else:
            result = create_user(username, password, address, port)

            if result == False:
                return False

            user_id = get_user_id(username)
            chats = get_chats(user_id)
            return chats
        
    def choose_chat(address: str, port: int, chat_name: str) -> list:
        chat_id = get_chat_id(chat_name)

        if not chat_id:
            return False
        
        set_chat(chat_id, datetime.now(), address, port)
        messages = get_message_history(chat_id)

        return messages
    
    def create_chat(address: int, port: int, username: str, chat_name: str):
        user_2_id = get_user_id(username)
        creator_id = get_user_id_by_session(address, port)

        if any([user_2_id, creator_id]) is None:
            return False
        
        result = create_chat(creator_id, chat_name, creator_id, user_2_id)

        if result == False:
            return False
        
        chat_id = get_chat_id(chat_name)

        if not chat_id:
            return False

        set_chat(chat_id, datetime.now(), address, port)
        messages = get_message_history(chat_id)
        return messages
    
    def send_message(address: str, port: int, text: str, ):
        author_name =   get_username(address, port)
        chat_id =       get_current_chat(address, port)
        result = create_message(chat_id, text, datetime.now(), author_name)

        if result == False:
            return False
        
        messages = get_message_history(chat_id)
        return messages
    
    state_processors = {
        'authorization':    authorization, 
        'login':            login,           # send chats
        'registration':     registration,    # send chats
        'main_menu':        choose_chat,     # send message history
        'chat_creation':    create_chat,     # send message history
        'in_chat':          send_message,    # update message history
    }

def process_request(request: str, address: str, port: int, state: str) -> tuple:
    """
    values:\n
    request: ответ клиента\n
    address, port: адрес и порт клиента\n
    state: состояние сессии
    returns: tuple\n
    new_state: новое состояние, если возникла ошибка обработки вернет текуее состояние\n
    bool: отвечате за возникновение ошибок False - ошибок не возникало\n
    data_to_send: данные которые нужн отправить клиенту\n
    """
    values = request.split(':')
    # проверяем не получили ли мы базовую команду
    if values[0] in list(basic_commands[values[0]].keys()):
        new_state = basic_commands[values[0]]
        return new_state, False, ''
        # при выходе командой назад нужно посылать данные 
        # либо придумать кэш на стороне клиента, так будет явно проще

    # проверяем не получили ли мы команду
    if values[0] in list(state_tree[state].keys()):
        new_state = state_tree[state][values[0]]
        return new_state, False, ''

    # если получены данные от клиента
    try:
        data_to_send = state_machine.state_processors[state](address, port, *values)
        if data_to_send == False:
            logging.error("возникла ошибка при вызове функции обработчика состояния, во время работы с базой данных")
            return state, True, ''
        new_state = state_tree[state]['DATA']
        return new_state, False, data_to_send
    except:
        logging.error("получены неверные данные от клиента")
        return state, True, '' 

server_errors = []
client_errors = []

if __name__ == "__main__":
    print(process_request(''))