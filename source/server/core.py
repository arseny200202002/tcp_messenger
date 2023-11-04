import asyncio
import configparser

async def handle_connection(reader, writer):

    address = writer.get_extra_info("peername")
    print(f"Connected by {address}")

    while True:
        try:
            data = await reader.read(1024)
        except ConnectionError:
            print(f"Client suddenly closed while receiving from {address}")
            break
        if not data:
            break
        data = data.upper()
        try:
            writer.write(data)
        except ConnectionError:
            print("Client suddenly closed, cannot send")
            break
        
    writer.close()
    print(f"Disconnected by {address}")

async def main(host, port):
    server = await asyncio.start_server(handle_connection, host, port)
    print("server successfully started")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("source\server\server_config.ini")

    asyncio.run(main(config["SERVER"]["SERVER_HOST"], config["SERVER"]["SERVER_PORT"]))


