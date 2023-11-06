import re

class requests:
    def data_request(data:list) -> str:
        request = "DATA" + ":"      
        for value in data:
            request += value   
            request += "|"          
        return request.encode()
    
    def command_request(command: str) -> str:
        request = "COMMAND" + ":"
        request += command
        return request.encode()

basic_commands = {'back': 'BACK',
                  'exit': 'EXIT'}

commands = {'sing_in': 'LOGIN',
            'sing_up': 'REGISTER',
            'create_chat': 'CREATE'}

def data_validation(num_of_values=1):
    def input_validation(func):
        def inner():
            input = func()
            if input is None: return 'error'
            if input in commands.values() or input in basic_commands.values():
                return requests.command_request(input)
            words = re.findall(r'\b\S+\b', input)
            if len(words) != num_of_values: return 'error'
            return requests.data_request(words)
        return inner
    return input_validation

class input_templates:
    @data_validation()
    def start() -> str:
        print(f"для входа введите: {commands['sing_in']}\nдля регистрации введите: {commands['sing_up']}")
        return input()

    @data_validation(num_of_values=2)
    def sing_in() -> str:
        print("введите логин и пароль\n")
        return input()
    @data_validation(num_of_values=3)
    def sing_up() -> str:
        print("введите логин, пароль и отображаемое имя: ")
        return input()
    @data_validation(num_of_values=1)
    def main() -> str:
        print(f"для создания чата введите: {commands['create_chat']}\n")
        print("для выбора чата введите его название: ")
        return input()
    @data_validation(num_of_values=2)
    def create_chat() -> str:
        print("введите имя пользователя, с которым вы хотите создать чат: ")
        username = input()

        print("введите название чата (можно оставить пустым):")
        chat_name = input()
        return username + ' ' + chat_name
    @data_validation(num_of_values=1)
    def send_message() -> str:
        print("введите текст сообщения: ")
        return input()

    templates = {'start':       start,
                 'sing_in':     sing_in,
                 'sing_up':     sing_up,
                 'main':        main,
                 'create_chat': create_chat,
                 'send_message':send_message}

client_error_messages = {'start':       "ОШИБКА: вероятно была введена неверная команда",
                         'sing_in':     "ОШИБКА: проверьте введенные данные",
                         'sing_up':     "ОШИБКА: проверьте введенные данные",
                         'main':        "ОШИБКА: введена невернаяя команда или неверное имя чата",
                         'create_chat': "ОШИБКА: проверьте введенные данные",
                         'send_message':"ОШИБКА: нельзя отправить пустое сообщение"}

server_error_messages = {'start':       "ОШИБКА: вероятно была введена неверная команда",
                         'sing_in':     "ОШИБКА: введены неверные данные",
                         'sing_up':     "ОШИБКА: пользователь с таким именем или логином уже существует",
                         'main':        "ОШИБКА: введена невернаяя команда или неверное имя чата",
                         'create_chat': "ОШИБКА: пользователся с таким именем не существует",
                         'send_message':"ОШИБКА: !!!требуется доработка!!!"}

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