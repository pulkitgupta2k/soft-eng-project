import socket
import random


def netcat(host, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, int(port)))
    s.sendall(content.encode())
    while True:
        data = s.recv(4096)
        if data:
            break
    s.close()
    return data.decode("utf-8")


def dev():
    PORT = 4444
    HOST = "0.0.0.0"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            while True:
                data = conn.recv(1024)
                if data:
                    data = data.decode("utf-8")
                    if data == "ON":
                        response = "Switched ON"
                    if data == "OFF":
                        response = "Switched OFF"
                    if data == "GET_TEMP":
                        response = str(f"Temperature is: {random.randint(20,30)}")
                if not data:
                    break
                conn.sendall(bytes(response, 'utf-8'))


if __name__ == "__main__":
    while True:
        dev()