import socket
import threading
from tkinter import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 2007))

running = True

def sendMsg():
    msg = msgInput.get()
    msgInput.delete(0, END)

    if msg:
        s.send(msg.encode())
        chatBox.insert(END, msg + "\n")

    if msg.lower() == "exit":
        closeApp()

def receiveMsg():
    global running
    while running:
        try:
            data = s.recv(1024)
            if not data:
                break
            chatBox.insert(END, data.decode() + "\n")
        except:
            break

def closeApp():
    global running
    running = False
    try:
        s.shutdown(socket.SHUT_RDWR)
    except:
        pass
    s.close()
    root.destroy()


root = Tk()
root.title("Python Chat App")

chatBox = Text(root, height=25, width=60)
chatBox.pack()

msgInput = Entry(root, width=50)
msgInput.pack()

sendBtn = Button(root, text="Send", command=sendMsg)
sendBtn.pack()

root.protocol("WM_DELETE_WINDOW", closeApp)


threading.Thread(target=receiveMsg, daemon=True).start()

root.mainloop()
