import socket
import threading
from tkinter import *
from tkinter.scrolledtext import ScrolledText

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 2007))

running = True

def sendMsg():
    msg = msgInput.get()
    msgInput.delete(0, END)

    if msg:
        s.send(msg.encode())
        chatBox.insert(END, msg + "\n", "me")
        chatBox.see(END)

    if msg.lower() == "exit":
        closeApp()

def receiveMsg():
    global running
    while running:
        try:
            data = s.recv(1024)
            if not data:
                break
            chatBox.insert(END, data.decode() + "\n","other")
            chatBox.see(END)
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
root.geometry("520x620")
root.configure(bg="#0f172a")

chatBox = ScrolledText(
    root,
    bg="#020617",
    fg="#e2e8f0",
    font=("Consolas", 11),
    wrap=WORD,
    padx=10,
    pady=10
)
chatBox.pack(padx=10, pady=10, fill=BOTH, expand=True)


bottom = Frame(root, bg="#0f172a")
bottom.pack(fill=X, padx=10, pady=5)

msgInput = Entry(
    bottom,
    bg="#1e293b",
    fg="white",
    insertbackground="white",
    font=("Consolas", 11)
)
msgInput.pack(side=LEFT, fill=X, expand=True, padx=(0,8))

sendBtn = Button(
    bottom,
    text="Send",
    bg="#2563eb",
    fg="white",
    activebackground="#1d4ed8",
    relief=FLAT,
    command=sendMsg   
)
sendBtn.pack(side=RIGHT)
msgInput.bind("<Return>", lambda e: sendMsg())

chatBox.tag_config("admin", foreground="#fbbf24")
chatBox.tag_config("me", foreground="#34d399")
chatBox.tag_config("other", foreground="#93c5fd")

chatBox.insert(END, "Admin: hello\n", "admin")

root.protocol("WM_DELETE_WINDOW", closeApp)


threading.Thread(target=receiveMsg, daemon=True).start()

root.mainloop()
