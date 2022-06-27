import socket


def start_client():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(("localhost", 2015))
    msg = "Hello, nigga!"
    server.send(msg.encode("utf-8"))
    response = server.recv(2015)
    print(response.decode("utf-8"))
    server.close()


if __name__ == "__main__":
    start_client()