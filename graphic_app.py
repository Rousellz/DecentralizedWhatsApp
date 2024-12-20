import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import requests
import json


class ChatApp:
    def __init__(self, root, LOCAL_IP, CLIENT_PORT):
        self.CLIENT_PORT = CLIENT_PORT
        self.url = f"http://{LOCAL_IP}:{self.CLIENT_PORT}"

        self.root = root
        self.root.title("WhatsApp-P2P")
        self.root.geometry("420x620")

        # Colores y estilos
        self.PRIMARY_COLOR = "#075E54"
        self.SECONDARY_COLOR = "#25D366"
        self.BACKGROUND_COLOR = "#ECE5DD"
        self.TEXT_LIGHT = "#FFFFFF"
        self.TEXT_DARK = "#212121"
        self.FONT_LARGE = ("Helvetica", 16, "bold")
        self.FONT_MEDIUM = ("Helvetica", 12)
        self.FONT_SMALL = ("Helvetica", 10)


        self.root.configure(bg=self.BACKGROUND_COLOR)
        self.current_frame = None

        self.session = requests.Session()  # Mantener la sesión activa con cookies
        self.create_main_widgets()

    def create_main_widgets(self):
        """Crea la pantalla principal de login/registro."""
        self.main_frame = tk.Frame(self.root, bg=self.BACKGROUND_COLOR)
        self.main_frame.pack(expand=True, padx=30, pady=30)

        title_label = tk.Label(
            self.main_frame,
            text="Bienvenido a WhatsApp-P2P",
            fg=self.PRIMARY_COLOR,
            bg=self.BACKGROUND_COLOR,
            font=self.FONT_LARGE,
        )
        title_label.pack(pady=(0, 30))

        tk.Label(
            self.main_frame, 
            text="Nickname:", 
            bg=self.BACKGROUND_COLOR, 
            font=self.FONT_MEDIUM,
            fg=self.TEXT_DARK
        ).pack(anchor="w", pady=5)
        self.nickname_entry = tk.Entry(self.main_frame, font=self.FONT_MEDIUM, bd=2, relief="groove")
        self.nickname_entry.pack(fill=tk.X, pady=5)

        tk.Label(
            self.main_frame, 
            text="Password:", 
            bg=self.BACKGROUND_COLOR, 
            font=self.FONT_MEDIUM,
            fg=self.TEXT_DARK
        ).pack(anchor="w", pady=5)
        self.password_entry = tk.Entry(self.main_frame, show="*", font=self.FONT_MEDIUM, bd=2, relief="groove")
        self.password_entry.pack(fill=tk.X, pady=5)

        button_frame = tk.Frame(self.main_frame, bg=self.BACKGROUND_COLOR)
        button_frame.pack(pady=20)

        tk.Button(
            button_frame,
            text="Register",
            command=self.register,
            bg=self.PRIMARY_COLOR,
            fg=self.TEXT_DARK,
            font=self.FONT_MEDIUM,
            activebackground=self.SECONDARY_COLOR,
        ).pack(side=tk.LEFT, padx=10, pady=10)

        tk.Button(
            button_frame,
            text="Login",
            command=self.login,
            bg=self.SECONDARY_COLOR,
            fg=self.TEXT_DARK,
            font=self.FONT_MEDIUM,
            activebackground=self.PRIMARY_COLOR,
        ).pack(side=tk.LEFT, padx=10, pady=10)

        self.current_frame = self.main_frame

    def switch_frame(self, new_frame):
        """Cambia entre marcos/pantallas."""
        if self.current_frame:
            self.current_frame.pack_forget()
        self.current_frame = new_frame
        self.current_frame.pack(expand=True, padx=20, pady=20)

    def create_back_button(self, parent, command):
        """Crea un botón de retorno."""
        back_button = tk.Button(
            parent,
            text="← Back",
            # command=lambda: threading.Thread(target=command).start(),
            command=command,
            fg=self.TEXT_DARK,
            bg=self.PRIMARY_COLOR,
            font=self.FONT_MEDIUM,
            activebackground=self.SECONDARY_COLOR,
        )
        back_button.pack(anchor="nw", pady=10, padx=10)

    def register(self):
        """Registra un nuevo usuario."""
        nickname = self.nickname_entry.get().strip()
        password = self.password_entry.get().strip()
        if not nickname or not password:
            messagebox.showerror("Error", "Nickname y Password son requeridos")
            return

        url = f"{self.url}/Register"
        response = self.session.post(
            url, params={"nickname": nickname, "password": password}
        )
        if response.status_code == 200:
            messagebox.showinfo("Éxito", response.text)
        else:
            messagebox.showerror("Error", response.text)

    def login(self):
        """Inicia sesión con un usuario existente."""
        nickname = self.nickname_entry.get().strip()
        password = self.password_entry.get().strip()
        if not nickname or not password:
            messagebox.showerror("Error", "Nickname y Password son requeridos")
            return

        url = f"{self.url}/Login"
        response = self.session.post(
            url, params={"nickname": nickname, "password": password}
        )
        if response.status_code == 200:
            messagebox.showinfo("Éxito", response.text)
            self.open_chats_window()
        else:
            messagebox.showerror("Error", response.text)

    def logout(self):
        """Cierra sesión."""
        url = f"{self.url}/Logout"
        response = self.session.post(url)
        if response.status_code == 200:
            messagebox.showinfo("Éxito", response.text)
            self.switch_frame(self.main_frame)
        else:
            messagebox.showerror("Error", response.text)

    def open_chats_window(self):
        """Abre la ventana de chats."""
        self.chats_frame = tk.Frame(self.root, bg=self.BACKGROUND_COLOR)
        self.create_back_button(self.chats_frame, self.logout)

        chats_label = tk.Label(
            self.chats_frame,
            text="Chats",
            bg=self.BACKGROUND_COLOR,
            font=self.FONT_LARGE,
        )
        chats_label.pack(pady=20)

        contacts_button = tk.Button(
            self.chats_frame,
            text="Contactos",
            command=self.open_contacts_window,
            bg=self.SECONDARY_COLOR,
            fg=self.TEXT_DARK,
            font=self.FONT_MEDIUM,
        )
        contacts_button.pack(pady=10)

        self.get_chats()
        self.switch_frame(self.chats_frame)

    def open_contacts_window(self):
        """Abre la ventana de contactos."""
        self.contacts_frame = tk.Frame(self.root, bg=self.BACKGROUND_COLOR)
        self.create_back_button(
            self.contacts_frame, lambda: self.switch_frame(self.chats_frame)
        )

        tk.Button(
            self.contacts_frame,
            text="Agregar Contacto",
            command=self.add_contact,
            bg=self.PRIMARY_COLOR,
            fg=self.TEXT_DARK,
            font=self.FONT_MEDIUM,
        ).pack(pady=10)

        tk.Button(
            self.contacts_frame,
            text="Eliminar Contacto",
            command=self.delete_contact,
            bg=self.PRIMARY_COLOR,
            fg=self.TEXT_DARK,
            font=self.FONT_MEDIUM,
        ).pack(pady=10)

        self.get_contacts()
        self.switch_frame(self.contacts_frame)

    def get_contacts(self):
        """Obtiene la lista de contactos del servidor."""
        url = f"{self.url}/GetContacts"
        response = self.session.get(url)
        if response.status_code == 200:
            contacts = response.json()
            for contact in contacts:
                name = contact["name"]
                nickname = contact["nickname"]
                tk.Button(
                    self.contacts_frame,
                    text=name,
                    command=lambda ch=nickname: self.open_chat_window(ch),
                    font=self.FONT_MEDIUM,
                ).pack(pady=5)
        else:
            messagebox.showerror("Error", response.text)

    def add_contact(self):
        """Agrega un nuevo contacto."""
        name = simpledialog.askstring(
            "Agregar Contacto", "Ingrese el nombre del contacto:"
        )
        nickname = simpledialog.askstring(
            "Agregar Contacto", "Ingrese el nickname del contacto:"
        )
        if not name or not nickname:
            messagebox.showerror("Error", "Nombre y nickname son requeridos")
            return
        url = f"{self.url}/AddContacts"
        response = self.session.post(url, params={"name": name, "nickname": nickname})
        if response.status_code == 200:
            messagebox.showinfo("Éxito", response.text)
            self.get_contacts()
        else:
            messagebox.showerror("Error", response.text)

    def delete_contact(self):
        """Elimina un contacto existente."""
        name = simpledialog.askstring(
            "Eliminar Contacto", "Ingrese el nombre del contacto a eliminar:"
        )
        if not name:
            messagebox.showerror("Error", "Nombre es requerido")
            return
        url = f"{self.url}/DeleteContacts"
        response = self.session.post(url, params={"name": name})
        if response.status_code == 200:
            messagebox.showinfo("Éxito", response.text)
            self.get_contacts()
        else:
            messagebox.showerror("Error", response.text)

    def get_chats(self):
        """Obtiene la lista de chats del servidor."""
        url = f"{self.url}/GetChats"
        response = self.session.get(url)
        if response.status_code == 200:
            chats = response.json()
            for chat in chats:
                tk.Button(
                    self.chats_frame,
                    text=chat,
                    command=lambda ch=chat: self.open_chat_window(ch),
                    font=self.FONT_MEDIUM,
                ).pack(pady=10)
        else:
            messagebox.showerror("Error", response.text)

    def open_chat_window(self, chat):
        """Abre una ventana de chat para un contacto."""
        self.chat_frame = tk.Frame(self.root, bg=self.BACKGROUND_COLOR)
        self.create_back_button(
            self.chat_frame, lambda: self.switch_frame(self.chats_frame)
        )

        chat_title = tk.Label(
            self.chat_frame,
            text=f"Chat con {chat}",
            bg=self.BACKGROUND_COLOR,
            font=self.FONT_LARGE,
        )
        chat_title.pack(pady=20)

        self.message_display = scrolledtext.ScrolledText(
            self.chat_frame, wrap=tk.WORD, font=self.FONT_MEDIUM, height=20
        )
        self.message_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.message_display.config(state=tk.DISABLED)

        self.get_messages(chat)

        entry_frame = tk.Frame(self.chat_frame, bg=self.BACKGROUND_COLOR)
        entry_frame.pack(fill=tk.X, pady=5)

        self.message_entry = tk.Entry(entry_frame, font=self.FONT_MEDIUM)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        tk.Button(
            entry_frame,
            text="Enviar",
            command=lambda: self.send_message(chat),
            bg=self.SECONDARY_COLOR,
            fg=self.TEXT_DARK,
            font=self.FONT_MEDIUM,
        ).pack(side=tk.RIGHT, padx=5)

        self.switch_frame(self.chat_frame)

    def get_messages(self, nickname):
        """Obtiene los mensajes de un chat."""
        url = f"{self.url}/GetMessages"
        response = self.session.get(url, params={"nickname": nickname})
        if response.status_code == 200:
            messages = response.json()
            self.message_display.config(state=tk.NORMAL)
            self.message_display.delete("1.0", tk.END)  # Limpiar mensajes anteriores
            for msg in messages:
                sender = msg["sender"]
                message = msg["message"]
                timestamp = msg["timestamp"]
                self.message_display.insert(
                    tk.END, f"{timestamp} - {sender}: {message}\n"
                )
            self.message_display.config(state=tk.DISABLED)
        else:
            messagebox.showerror("Error", response.text)

    def send_message(self, user):
        """Envía un mensaje a un usuario."""
        message = self.message_entry.get().strip()
        if not message:
            return
        url = f"{self.url}/SendMessage"
        response = self.session.post(url, params={"user": user, "message": message})
        if response.status_code == 200:
            self.message_entry.delete(0, tk.END)
            self.get_messages(user)  # Actualizar mensajes después de enviar
        else:
            messagebox.showerror("Error", response.text)


if __name__ == "__main__":
    LOCAL_IP = "127.0.0.1"
    CLIENT_PORT = 5000  # Asegurarse de que coincida con el puerto del servidor
    root = tk.Tk()
    app = ChatApp(root, LOCAL_IP, CLIENT_PORT)
    root.mainloop()


