import re

def parse_responce(text: str) -> list:
    index = 0
    size = len(text)
    strings = []
    string = ''
    while index < size:
        if text[index] != '<': 
            string += text[index]
            index += 1
            continue
        else:
            if string != '': strings.append(string)
            start = index
            
            while text[index] != '>': index += 1
            index += 1
            keyword = text[start:index]
            strings.append(keyword)
            string = ''
    return strings

def prosess_responce(fields: list) -> list:
    user_data = []
    for i, field in enumerate(fields):
        if field == '<text>':
            print(fields[i+1])
        if field == '<input>':
            while True:
                data = input()
                words = re.findall(r'\b\S+\b', data)
                if len(words) == 0:
                    print("!!!input data can't be blank!!!")
                else:
                    user_data.append(data)
                    break
    return user_data

def create_request(user_data: list) -> bytes:
    request = ''
    for data in user_data:
        request += data
        request += ':'
    return request.encode()