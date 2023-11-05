
def encode_request(func):
    def inner(*args, **kwargs):
        request = func(*args, **kwargs)
        request.encode('utf-8')
        return request
    return inner

class requests:
    special_symbols = {"start_request": ":",
                       "data_separator": "|",
                       "end_request": ";"}

    @encode_request
    def initialization_request() -> str:
        request = "START" + ";"
        return request
    def data_request(data:list) -> str:
        request = "DATA" + ":"      # keyword for request containing data
        for value in data:
            request += str(value)   # value
            request += "|"          # separator of data
        request += ";"              # means end of request
        return request
    def command_request(command: str) -> str:
        request = "COMMAND" + ":"
        request += command
        request += ";"


class answer_templates:
    answers = {"": 1,
               "": 2,
               "": 3}
    pass