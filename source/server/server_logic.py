from db.db_requests import *

state_tree = [
    [1, 2],
    [3],
    [3],
    [4, 5],
    [6],
    [6],
]

backward_state_tree = [
    0,
    0,
    0,
    3,
    3,
    3,
    5,
]

state_names = {
    0: 'start',
    1: 'sing_in',
    2: 'sing_up',
    3: 'main',
    4: 'create_chat',
    5: 'choose_chat',
    6: 'send_message',
}


class state_machine:
    def start(address):
        now = datetime.now()
        session = Sessions(is_guest=True, last_update_time=now, state=0, address=address)
        create_session(session)

    def sing_in(login, password, state): # state = 1
        user_exists = check_sing_in(login, password)
        if user_exists:
            user_id = get_user_id(login)
            update_session(user_id=user_id, state=state_names[state], time=datetime.now())
            return True
        else:
            return False
        
    def sing_up(login, password, username, state):
        user_exists = check_sing_in(login, password)

        if user_exists == True:
            return False
        
        user = Users(username=username, password_hash=password, login=login)
        create_user(user)
        #user_id = get_user_id(login)
        update_session(user_id=user.id, state=state_names[state], time=datetime.now())
        return True
    
    def main(data):
        pass    
    def create_chat(data):
        chat = Chats()
        create_chat(chat, )
    def choose_chat(data):
        pass
    def send_message(data):
        chat_id = data
        #message = Messages(text=text, send_date=send_date, author_name=author_name)
        #create_message(chat_id, message)
        
    state_functions = {
        'start': start,
        'sing_in': sing_in,
        'sing_up': sing_up,
        'main': main,
        'create_chat': create_chat,
        'choose_chat': choose_chat,
        'send_message': send_message,
    }