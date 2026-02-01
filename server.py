# server

import socket
import threading


def clientHandler(conn, name):
    namemsg = f"Admin: Hi {name}, Welcome to my chatroom"
    conn.send(namemsg.encode())
    print(f"{name} joined the chat")
    for client in clients:
        if client[1] == conn:
            continue
        msg_to_send = f"{name} joined the chat".encode()
        client[1].send(msg_to_send)

    while True:
        msg = conn.recv(1024)
        # print(msg)
        for client in clients:
            if client[1] == conn:
                continue
            msg_to_send = f"{name}: {msg.decode()}".encode()
            client[1].send(msg_to_send)

        if msg.decode() == "exit" or not msg:
            clients.remove((name, conn))
            break

    conn.close()


clients = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(("localhost", 2007))
s.listen(5)
print("Listening...")



while True:
    conn, addr = s.accept()
    name = conn.recv(1024).decode()
    clients.append((name, conn))
    threading.Thread(target=clientHandler, args=(conn, name)).start()


s.close()
