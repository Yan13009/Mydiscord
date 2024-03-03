import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox
import socket
import threading
import json
import os

class ChatClient(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chat Client")
        self.nickname = "Anonymous"  # Initialiser self.nickname avec une valeur par défaut
        self.client = None
        self.stop_thread = False
        self.initialize_gui()

    def initialize_gui(self):
        self.text_area = scrolledtext.ScrolledText(self)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        self.msg_entry = tk.Entry(self)
        self.msg_entry.pack(padx=20, pady=5, fill=tk.X)

        self.send_button = tk.Button(self, text="Send", command=self.write)
        self.send_button.pack(padx=20, pady=5)

    def load_servers(self):
        try:
            with open('servers.json') as f:
                self.servers = json.load(f)
        except FileNotFoundError:
            self.servers = {}
            messagebox.showwarning("Warning", "servers.json not found. Please add a server.")

    def add_server(self, name, ip, port):
        self.servers[name] = {"10.10.77.63": ip, "50000": port}
        with open('servers.json', 'w') as f:
            json.dump(self.servers, f, indent=4)

    def enter_server(self):
        server_name = simpledialog.askstring("Enter Server", "Enter the server name:")
        if server_name in self.servers:
            self.nickname = simpledialog.askstring("Nickname", "Choose your nickname:")
            if self.nickname == 'admin':
                self.password = simpledialog.askstring("Password", "Enter password for admin:", show='*')
            
            server_info = self.servers[server_name]
            self.connect_to_server(server_info['ip'], server_info['port'])
        else:
            messagebox.showerror("Error", "Server not found.")

    def connect_to_server(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect((ip, port))
            self.stop_thread = False
            threading.Thread(target=self.receive).start()
        except ConnectionRefusedError:
            messagebox.showerror("Connection Error", "Unable to connect to the server.")

    def receive(self):
        while not self.stop_thread:
            try:
                message = self.client.recv(1024).decode('ascii')
                if message == 'NICK':
                    self.client.send(self.nickname.encode('ascii'))
                    next_message = self.client.recv(1024).decode('ascii')
                    if next_message == 'PASS':
                        self.client.send(self.password.encode('ascii'))
                        if self.client.recv(1024).decode('ascii') == 'REFUSE':
                            messagebox.showerror("Error", "Connection refused! Wrong password.")
                            self.stop_thread = True
                    elif next_message == 'BAN':
                        messagebox.showerror("Error", "Connection refused due to ban.")
                        self.stop_thread = True
                else:
                    self.display_message(message)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
                self.client.close()
                break

    def write(self):
        if self.client is None:
            messagebox.showerror("Connection Error", "Not connected to a server.")
            return

        message = f'{self.nickname}: {self.msg_entry.get()}'
        self.client.send(message.encode('ascii'))
        self.msg_entry.delete(0, tk.END)

    def display_message(self, message):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.yview(tk.END)
        self.text_area.config(state='disabled')

if __name__ == "__main__":
    app = ChatClient()
    app.protocol("WM_DELETE_WINDOW", app.quit)
    app.mainloop()
