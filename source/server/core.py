import os 
import sys 
cwd = os.getcwd() 
sys.path.append(cwd)

import asyncio
import configparser
from db.db_requests import *
from server_logic import *

async def handle_connection(reader, writer):
    # accepted connection
    address, port = writer.get_extra_info("peername")

    print(f"Connected by address: {address} port: {port}")

    # get state of possible session from that address
    state = get_state(address, port)

    # if its new connection from that address create session
    if state is None: 
        now = datetime.now()
        create_session(now, address, port)
        request = 'TEMPLATE:' + 'authorization'
        state = 0
        
    # else send needed template to client
    else:
        request = 'TEMPLATE:' + state_names[state]

    writer.write(request.encode())
        
    while True:
        try:
            # read client responce
            data = await reader.read(1024)

            if not data: break

            data = data.decode()
            # understand client responce
            state = get_state(address, port)
            response = parse_responce(data)
            new_state, request = process_responce(address, port, state, response)

            if request == 'ERROR':
                logging.error(f"we send ERROR request to client")

            if new_state != state: # если состояние изменилось - обновляем сессию
                update_session(new_state, datetime.now(), address, port)

        except ConnectionError:
            print(f"Client suddenly closed while receiving from {address} {port}")
            break

        try:
            # отправляем запрос
            writer.write(request.encode())
        except ConnectionError:
            print("Client suddenly closed, cannot send")
            break
        
    writer.close()
    update_session(0, datetime.now(), address, port)
    print(f"Disconnected by address: {address} port: {port}")



async def main(host, port):
    server = await asyncio.start_server(handle_connection, host, port)
    print("server successfully started")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("source\server\server_config.ini")
    host = config["SERVER"]["SERVER_HOST"]
    port = config["SERVER"]["SERVER_PORT"]

    logging.basicConfig(level=logging.INFO, filename="server_log.log",filemode="w")

    asyncio.run(main(host, port))


