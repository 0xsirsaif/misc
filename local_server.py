import socket
import contextlib


def do_something(client):
    request = client.recv(2015)
    print(request)
    try:
        response = "Hello, dead!".encode("utf-8")
    except (ValueError, KeyError) as ex:
        response = repr(ex).encode("utf-8")
    client.send(response)


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 2015))
    server.listen(1)
    with contextlib.closing(server):
        while True:
            client, address = server.accept()
            do_something(client)
            client.close()


if __name__ == "__main__":
    start_server()