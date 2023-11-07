import re

class requests:
    def data_request(data:list) -> str:
        request = "DATA" + ":"      
        for value in data:
            request += value   
            request += "|"          
        return request[:-1].encode()
    
    def command_request(command: str) -> str:
        request = "COMMAND" + ":"
        request += command
        return request.encode()

basic_commands = {
    'BACK': 'BACK',
    'EXIT': 'EXIT',
    }

commands = {
    'login':            'LOGIN',
    'register':         'REGISTER',
    'chat_creation':    'CREATE',
    }

def data_validation(num_of_values=1):
    def input_validation(func):
        def inner():
            input = func()
            if input is None: return 'error'
            if input in commands.values() or input in basic_commands.values():
                return requests.command_request(input)
            words = re.findall(r'\b\S+\b', input)
            if len(words) != num_of_values:
                return 'error'
            return requests.data_request(words)
        return inner
    return input_validation

class input_templates:
    @data_validation()
    def authorization() -> str:
        print(f"для входа введите: {commands['login']}\nдля регистрации введите: {commands['register']}")
        return input()

    @data_validation(num_of_values=2)
    def login() -> str:
        print("введите логин и пароль\n")
        return input()
    
    @data_validation(num_of_values=3)
    def register() -> str:
        print("введите логин, пароль и отображаемое имя: ")
        return input()
    
    @data_validation(num_of_values=1)
    def main_menu() -> str:
        print(f"для создания чата введите: {commands['chat_creation']}\n")
        print("для выбора чата введите его название: ")
        return input()
    
    @data_validation(num_of_values=2)
    def chat_creation() -> str:
        print("введите имя пользователя, с которым вы хотите создать чат: ")
        username = input()

        print("введите название чата (можно оставить пустым):")
        chat_name = input()
        return username + ' ' + chat_name
    
    @data_validation(num_of_values=1)
    def in_chat() -> str:
        print("введите текст сообщения: ")
        return input()

    templates = {
        'authorization':    authorization,
        'login':            login,
        'register':         register,
        'main_menu':        main_menu,
        'chat_creation':    chat_creation,
        'in_chat':          in_chat,
        }

client_error_messages = {
    'authorization':        "ОШИБКА: вероятно была введена неверная команда",
    'login':                "ОШИБКА: проверьте введенные данные",
    'register':             "ОШИБКА: проверьте введенные данные",
    'main_menu':            "ОШИБКА: введена невернаяя команда или неверное имя чата",
    'chat_creation':        "ОШИБКА: проверьте введенные данные",
    'in_chat':              "ОШИБКА: нельзя отправить пустое сообщение",
}

server_error_messages = {
    'authorization':        "ОШИБКА: вероятно была введена неверная команда",
    'login':                "ОШИБКА: введены неверные данные",
    'register':             "ОШИБКА: пользователь с таким именем или логином уже существует",
    'main_menu':            "ОШИБКА: введена невернаяя команда или неверное имя чата",
    'chat_creation':        "ОШИБКА: пользователся с таким именем не существует",
    'in_chat':              "ОШИБКА: !!!требуется доработка!!!",
}

class server_answer:
    def __init__(self, template:str = None, data:list = None):
        self.template = template
        self.data = data

    def __eq__(self, __value: object) -> bool:
        if self.template == __value.template and self.data == __value.data:
            return True
        else:
            return False

def parse_server_answer(raw_string) -> server_answer:
    words = raw_string.split(':')
    if words[0] == 'ERROR': return server_answer('error')
    if words[0] != 'TEMPLATE': return server_answer('error')

    template = words[1]
    if len(words) == 2: return server_answer(template)

    if words[2] == 'DATA':
        data = []
        for word in words[3:]:
            data.append(word)
    return server_answer(template, data)