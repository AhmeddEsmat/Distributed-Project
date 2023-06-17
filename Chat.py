import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog


class Client:
    def __init__(self, host, port, username):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(("localhost", 7000))

        msg = tkinter.Tk()
        msg.withdraw()

        self.username = username
        self.gui_done = False
        self.running = True
        self.gui_thread = threading.Thread(target=self.gui_loop)
        self.receive_thread = threading.Thread(target=self.receive)
        self.gui_thread.daemon = True
        self.gui_thread.start()
        self.receive_thread.start()

    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg="#363636")  # Set the background color to dark grey (#363636)
        self.win.title("Chatroom")  # Set the title of the window to "Chatroom"

        self.chat_label = tkinter.Label(self.win, text="Live Chat", bg="#363636", fg="white")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=10, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win, bg="#D8D8D8", fg="black", width=40)
        self.text_area.pack(padx=10, pady=5)
        self.text_area.config(state='disabled')

        self.input_area = tkinter.Text(self.win, height=3, bg="#D8D8D8", fg="black", width=40)
        self.input_area.pack(padx=10, pady=5)

        self.send_button = tkinter.Button(self.win, text="Send", command=self.write, bg="#ECECEC", fg="black",
                                          relief=tkinter.SOLID, bd=0, highlightthickness=0)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=10, pady=5)

        # Apply rounded corners to the button
        self.send_button.configure(borderwidth=0, highlightthickness=0, relief=tkinter.FLAT)
        self.send_button.update_idletasks()
        radius = 15
        width = self.send_button.winfo_width()
        height = self.send_button.winfo_height()
        self.send_button.configure(
            highlightbackground=self.send_button["background"],
            bd=0,
            highlightthickness=0,
            relief=tkinter.FLAT
        )
        self.send_button.bind("<Enter>", lambda event: self.send_button.configure(background="#D8D8D8"))
        self.send_button.bind("<Leave>", lambda event: self.send_button.configure(background="#ECECEC"))

        self.gui_done = True
        self.win.protocol("WM_DELETE_WINDOW", self.stop)
        self.win.geometry("400x600")
        self.win.mainloop()

    def write(self):
        message = f"{self.username}: {self.input_area.get('1.0', 'end')}"
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024)
                if message == 'enter player username: ':
                    self.sock.send(self.username.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break