import requests

class UI:
    def __init__(self, LOCAL_IP, CLIENT_PORT):
        self.CLIENT_PORT = CLIENT_PORT
        self.url = f"http://{LOCAL_IP}:{self.CLIENT_PORT}"


    def register(self, nickname, password):

        url = f"{self.url}/Register"

        response = requests.post(url, params={"nickname": nickname, "password": password})
        
        if response.status_code == 200:
            print(f"Mensaje recibido: {response.text}")
        else:
            print(f"Error: {response.status_code}")


    def login(self, nickname, password):
        url = f"{self.url}/Login"

        response = requests.post(url, params={"nickname": nickname, "password": password})

        if response.status_code == 200:
            print(f"Mensaje recibido: {response.text}")
        else:
            print(f"Error: {response.status_code}")


    def logout(self):
        url = f"{self.url}/Logout"

        response = requests.post(url)

        if response.status_code == 200:
            print(f"Mensaje recibido: {response.text}")
        else:
            print(f"Error: {response.status_code}")


    def get_contacts(self):
        url = f"{self.url}/GetContacts"

        response = requests.get(url)

        if response.status_code == 200:
            print(f"Mensaje recibido: {response.text}")
        else:
            print(f"Error: {response.status_code}")


    def add_contact(self, name, nickname):
        url = f"{self.url}/AddContacts"

        response = requests.post(url, params={"name": name, "nickname": nickname})

        if response.status_code == 200:
            print(f"Mensaje recibido: {response.text}")
        else:
            print(f"Error: {response.status_code}")

    
    def delete_contact(self, name):
        url = f"{self.url}/DeleteContacts"

        response = requests.post(url, params={"name": name})

        if response.status_code == 200:
            print(f"Mensaje recibido: {response.text}")
        else:
            print(f"Error: {response.status_code}")


    def get_chats(self):
        url = f"{self.url}/GetChats"

        response = requests.get(url)

        if response.status_code == 200:
            print(f"Mensaje recibido: {response.text}")
        else:
            print(f"Error: {response.status_code}")


    def send_message(self, user, message):
        url = f"{self.url}/SendMessage"

        response = requests.post(url, params={"user": user, "message": message})

        if response.status_code == 200:
            print(f"Mensaje recibido: {response.text}")
        else:
            print(f"Error: {response.status_code}")

    
    def get_messages(self, nickname):
        url = f"{self.url}/GetMessages"

        response = requests.get(url, params={"nickname": nickname})

        if response.status_code == 200:
            print(f"Mensaje recibido: {response.text}")
        else:
            print(f"Error: {response.status_code}")


    def start(self):
        print("help: ayuda")
        print("register: registrar un usuario")
        print("login: iniciar sesion")
        print("logout: cerrar sesion")
        print("get_contacts: obtener contactos")
        print("add_contact: agregar contacto")
        print("delete_contact: eliminar contacto")
        print("get_chats: obtener chats")
        print("send_message: enviar mensaje")
        print("get_messages: obtener mensajes")
        print("exit: salir")
        while(True):
            command = input("Ingrese el comando: ")
            if command == "help":
                print("register: registrar un usuario")
                print("login: iniciar sesion")
                print("logout: cerrar sesion")
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
                break