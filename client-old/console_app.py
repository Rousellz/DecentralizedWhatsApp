import requests


class UI:
    def __init__(self, LOCAL_IP, CLIENT_PORT):
        self.CLIENT_PORT = CLIENT_PORT
        self.url = f"http://{LOCAL_IP}:{self.CLIENT_PORT}"
        self.session = (
            requests.Session()
        )  # Para mantener la sesión activa con el servidor

    def register(self, nickname, password):
        url = f"{self.url}/Register"
        response = self.session.post(
            url, params={"nickname": nickname, "password": password}
        )
        if response.status_code == 200:
            print(f"Mensaje recibido: {response.text}")
        else:
            print(f"Error: {response.text}")

    def login(self, nickname, password):
        url = f"{self.url}/Login"
        response = self.session.post(
            url, params={"nickname": nickname, "password": password}
        )
        if response.status_code == 200:
            print(f"Mensaje recibido: {response.text}")
        else:
            print(f"Error: {response.text}")

    def logout(self):
        url = f"{self.url}/Logout"
        response = self.session.post(url)
        if response.status_code == 200:
            print(f"Mensaje recibido: {response.text}")
        else:
            print(f"Error: {response.text}")

    def get_contacts(self):
        url = f"{self.url}/GetContacts"
        response = self.session.get(url)
        if response.status_code == 200:
            contacts = response.json()
            print("Contactos:")
            for contact in contacts:
                print(f"Nombre: {contact['name']}, Nickname: {contact['nickname']}")
        else:
            print(f"Error: {response.text}")

    def add_contact(self, name, nickname):
        url = f"{self.url}/AddContacts"
        response = self.session.post(url, params={"name": name, "nickname": nickname})
        if response.status_code == 200:
            print(f"Mensaje recibido: {response.text}")
        else:
            print(f"Error: {response.text}")

    def delete_contact(self, name):
        url = f"{self.url}/DeleteContacts"
        response = self.session.post(url, params={"name": name})
        if response.status_code == 200:
            print(f"Mensaje recibido: {response.text}")
        else:
            print(f"Error: {response.text}")

    def get_chats(self):
        url = f"{self.url}/GetChats"
        response = self.session.get(url)
        if response.status_code == 200:
            chats = response.json()
            print("Chats:")
            for chat in chats:
                print(f"- {chat}")
        else:
            print(f"Error: {response.text}")

    def send_message(self, user, message):
        url = f"{self.url}/SendMessage"
        response = self.session.post(url, params={"user": user, "message": message})
        if response.status_code == 200:
            print(f"Mensaje recibido: {response.text}")
        else:
            print(f"Error: {response.text}")

    def get_messages(self, nickname):
        url = f"{self.url}/GetMessages"
        response = self.session.get(url, params={"nickname": nickname})
        if response.status_code == 200:
            messages = response.json()
            print(f"Mensajes con {nickname}:")
            for msg in messages:
                print(f"{msg['timestamp']} - {msg['sender']}: {msg['message']}")
        else:
            print(f"Error: {response.text}")

    def start(self):
        print("Bienvenido al cliente de mensajería")
        print("Comandos disponibles:")
        print("help: mostrar ayuda")
        print("register: registrar un usuario")
        print("login: iniciar sesión")
        print("logout: cerrar sesión")
        print("get_contacts: obtener contactos")
        print("add_contact: agregar contacto")
        print("delete_contact: eliminar contacto")
        print("get_chats: obtener chats")
        print("send_message: enviar mensaje")
        print("get_messages: obtener mensajes")
        print("exit: salir")
        while True:
            command = input("Ingrese el comando: ")
            if command == "help":
                print("Comandos disponibles:")
                print("register: registrar un usuario")
                print("login: iniciar sesión")
                print("logout: cerrar sesión")
                print("get_contacts: obtener contactos")
                print("add_contact: agregar contacto")
                print("delete_contact: eliminar contacto")
                print("get_chats: obtener chats")
                print("send_message: enviar mensaje")
                print("get_messages: obtener mensajes")
                print("exit: salir")
            elif command == "register":
                nickname = input("Ingrese su nickname: ")
                password = input("Ingrese su password: ")
                self.register(nickname, password)
            elif command == "login":
                nickname = input("Ingrese su nickname: ")
                password = input("Ingrese su password: ")
                self.login(nickname, password)
            elif command == "logout":
                self.logout()
            elif command == "get_contacts":
                self.get_contacts()
            elif command == "add_contact":
                name = input("Ingrese el nombre del contacto: ")
                nickname = input("Ingrese el nickname del contacto: ")
                self.add_contact(name, nickname)
            elif command == "delete_contact":
                name = input("Ingrese el nombre del contacto: ")
                self.delete_contact(name)
            elif command == "get_chats":
                self.get_chats()
            elif command == "send_message":
                user = input("Ingrese el usuario al que desea enviar el mensaje: ")
                message = input("Ingrese el mensaje: ")
                self.send_message(user, message)
            elif command == "get_messages":
                nickname = input("Ingrese el nickname del contacto: ")
                self.get_messages(nickname)
            elif command == "exit":
                print("Saliendo del cliente...")
                break
            else:
                print(
                    "Comando no reconocido. Escriba 'help' para ver los comandos disponibles."
                )


if __name__ == "__main__":
    LOCAL_IP = "10.0.11.10"
    CLIENT_PORT = 5000  # Asegúrate de que coincida con el puerto del servidor
    ui = UI(LOCAL_IP, CLIENT_PORT)
    ui.start()

