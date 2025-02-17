import json
from database.data_client import DataBaseClient
from src.service.heartbeat import HeartBeatManager
from network_utils import get_ip, SERVICE_PORT
from .client_utils import SERVER_ADDRESSES_CACHE_FILENAME

class ClientInstance:
    """
    Represents a client instance for a messaging application.

    Attributes:
        user (dict): A dictionary containing user information.
        login (bool): A boolean indicating whether the user is logged in or not.
        manager (HeartBeatManager): An instance of the HeartBeatManager class.
        ip (str): The IP address of the client.
        port (int): The port number of the client.
        database (DataBaseClient): An instance of the DataBaseClient class.

    Methods:
        login_user: Logs in the user with the given nickname and password.
        logout_user: Logs out the user.
        update_servers: Updates the status of the servers.
        save_nodes: Saves the information of the servers to a file.
        save_info: Saves the given data to a file.
        get_contacts: Retrieves the contacts of the user.
        add_contacts: Adds a new contact for the user.
        update_contact: Updates the information of a contact.
        contain_contact: Checks if a contact exists.
        delete_contact: Deletes a contact.
        get_name: Retrieves the name of a contact.
        get_nickname: Retrieves the nickname of a contact.
        get_messages: Retrieves all messages.
        add_messages: Adds a new message.
        delete_messages: Deletes a message.
        search_messages_from: Searches for messages sent from a user.
        search_messages_to: Searches for messages sent to a user.
        get_chats: Retrieves all chats of the user.
        add_chat: Adds a new chat between two users.
        search_chat_id: Searches for the chat ID between two users.
        delete_chat: Deletes a chat between two users.
        search_chat: Searches for a chat with a specific user.
    """

    def __init__(self):
        self.user = {}
        self.login = False
        self.manager = HeartBeatManager()
        self.ip = get_ip()
        self.port = SERVICE_PORT
        self.database = DataBaseClient()

    def login_user(self, nickname: str, password: str):
        self.user['nickname'] = nickname
        self.user['password'] = password
        self.login = True

    def logout_user(self):
        self.user = {}
        self.login = False

    def update_servers(self):
        self.manager.check_health()

    def save_nodes(self):
        nodes = [node.serialize() for node in self.manager.get_nodes()]
        self.save_info(SERVER_ADDRESSES_CACHE_FILENAME, nodes)

    def save_info(self, file_name, data: list):
        with open(file_name, "w") as j:
            json.dump(data, j, indent=2)

    def get_contacts(self):
        return [(nickname, name) for (nickname, name) in self.database.get_contacts(self.user['nickname'])]

    def add_contacts(self, nickname: str, name: str):
        return self.database.add_contacts(self.user['nickname'], nickname, name)

    def update_contact(self, nickname: str, name: str):
        return self.database.update_contact(self.user['nickname'], nickname, name)

    def contain_contact(self, nickname: str):
        return self.database.contain_contact(self.user['nickname'], nickname)

    def delete_contact(self, nickname: str):
        return self.database.delete_contact(self.user['nickname'], nickname)

    def get_name(self, nickname: str):
        return self.database.get_name(self.user['nickname'], nickname)

    def get_nickname(self, name: str):
        return self.database.get_nickname(self.user['nickname'], name)

    def get_messages(self):
        return self.database.get_messages()

    def add_messages(self, source: str, destiny: str, value: str, id: int = -1):
        return self.database.add_messages(source, destiny, value, id)

    def delete_messages(self, id_message: int):
        return self.database.delete_messages(id_message)

    def search_messages_from(self, me: str, user: str):
        return self.database.search_messages_from(me, user)

    def search_messages_to(self, me: str, user: str):
        return self.database.search_messages_to(me, user)

    def get_chats(self):
        return self.database.get_chats(self.user['nickname'])

    def add_chat(self, user_id_1_: str, user_id_2_: str):
        return self.database.add_chat(user_id_1_, user_id_2_)

    def search_chat_id(self, user_id_1: str, user_id_2: str):
        return self.database.search_chat_id(user_id_1, user_id_2)

    def delete_chat(self, user_id_1: str, user_id_2: str):
        return self.database.delete_chat(user_id_1, user_id_2)

    def search_chat(self, user_id_2: str):
        return self.database.search_chat(self.user['nickname'], user_id_2)
