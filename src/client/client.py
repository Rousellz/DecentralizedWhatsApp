from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Union
from src.server.identity.remote_identity_node import RemoteIdentityNode
from src.service.requests import RequestManager
from network_utils import SERVER_PORT
from .client_instance import ClientInstance
from .client_utils import *

service = FastAPI(docs_url=None)
client_api = FastAPI()
client = ClientInstance()


@client_api.post("/Register")
def register(nickname: str, password: str, request: Request):
    client: ClientInstance = request.state.client
    
    if client.login:
        return "You are logged"

    server_node = RemoteIdentityNode.from_base_node(
        client.manager.get_random_node())

    try:
        nodes = server_node.all_nodes()
        client.manager.add_nodes(*nodes)
    except:
        return "Server Error"

    node = server_node.search_identity_node(nickname)

    if node is not None:
        node_data = node.nickname_identity_node(nickname, -1)

        if node_data is not None:
            return "You are already registered"
        else:  
            success = register_user(node, nickname,
                                    password, client.ip, client.port)
            if success is False:
                return "Register error"

            client.login_user(nickname, password)
            return 'Register complete'
    else:
        return "Please register again"


@client_api.post("/Login")
def login(nickname: str, password: str, request: Request):
    client: ClientInstance = request.state.client
    if client.login:
        return 'You are logged'

    server_node = RemoteIdentityNode.from_base_node(
        client.manager.get_random_node())

    try:
        nodes = server_node.all_nodes()
        client.manager.add_nodes(*nodes)
    except:
        return "Server Error"

    try:
        node = server_node.search_identity_node(nickname)
    except:
        return "Server Error"

    node_data: Union[BaseIdentityNode, None] = None

    try:
        if node is not None:
            node_data = node.nickname_identity_node(nickname, -1)
            if node_data is None:
                return "You are not registered"
    except:
        return "Login error"

    if node_data is not None:
        try:
            password_server = node_data.get_pasword(nickname, -1)
            if password_server is not None and password != password_server:
                return "Wrong password"

            node_data.update_user(nickname, client.ip, client.port, -1)

            client.login_user(nickname, password)

            task_receive_message(client.user['nickname'], client.database,
                                 node_data)
            return 'Login Successful'
        except Exception as e:
            return "Login error"


@client_api.post("/Logout")
def logout(request: Request):
    client: ClientInstance = request.state.client
    client.logout_user()
    return 'Logout Successful'


@client_api.get("/GetContacts")
def get_contacts(request: Request):
    client: ClientInstance = request.state.client
    if not client.login:
        return "You are not logged"
    result = {}
    contacts = client.get_contacts()
    for contact in contacts:
        result[contact[1]] = contact[0]
    return result


@client_api.post("/AddContacts")
def add_contacts(name: str, nickname: str, request: Request):
    client: ClientInstance = request.state.client

    if not client.login:
        return "You are not logged"

    servers = client.manager.get_nodes()

    if len(servers) == 0:
        return 'Lost connection, you need to login again'

    node_data = RemoteIdentityNode.from_base_node(
        client.manager.get_random_node())

    dict_other_user = node_data.nickname_identity_node(nickname, -1)
    if dict_other_user is None:
        return nickname+" "+"is not register"

    if client.add_contacts(nickname, name):
        return 'Contact Added'


@client_api.post("/DeleteContacts")
def delete_contacts(name: str, request: Request):
    client: ClientInstance = request.state.client
    if not client.login:
        return "You are not logged"

    nickname = client.get_nickname(name)
    if nickname is None:
        nickname = name

    if client.delete_contact(nickname):
        return 'Contact Deleted'
    else:
        return "The contact"+" " + name + " " + "does not exist"


@client_api.get("/GetMessages")
def get_messages(nickname: str, request: Request):  
    client: ClientInstance = request.state.client
    if not client.login:
        return "You are not logged"

    servers = client.manager.get_nodes()

    if len(servers) == 0:
        return 'Lost connection, you need to login again'

    nickname_other_user = client.get_nickname(nickname)

    if nickname_other_user is None:
        nickname_other_user = nickname
        name = client.get_name(nickname)

        if name is None:
            name = nickname
    else:  
        name = nickname

    mynickname = client.user['nickname']
    messages = client.search_chat(nickname_other_user)

    messages_format = []
    for message in messages:
        if message[0] == mynickname:
            messages_format.append('me' + ": " + message[1])
        else:
            messages_format.append(
                name + ": " + message[1])
    return messages_format

@client_api.post("/SendMessage")
def send(user: str, message: str, request: Request):
    client: ClientInstance = request.state.client
    if not client.login:
        return "You are not logged"

    servers = client.manager.get_nodes()

    if len(servers) == 0:
        return 'Lost connection, you need to login again'

    nickname_user = client.get_nickname(user)
    if nickname_user is None:
        nickname_user = user

    node_data = RemoteIdentityNode.from_base_node(
        client.manager.get_random_node())

    dict_other_user = node_data.nickname_identity_node(nickname_user, -1)
    if dict_other_user is None:
        return user+" "+"is not register"
    my_nickname = client.user['nickname']

    try:
        ip, port = dict_other_user.get_ip_port(nickname_user, -1).split(":")
        rm = RequestManager(ip, port)
        rm.post("/ReceiveMessage", params={
            "nickname_from": my_nickname, "nickname_to": nickname_user, 'value': message})
    except:
        if add_message(dict_other_user, my_nickname, nickname_user, message) is False:
            return 'send failed'

    client.add_messages(my_nickname, nickname_user, message, -1)
    return "Send Message"


@client_api.get("/GetChats")
def get_chats(request: Request):
    client: ClientInstance = request.state.client
    if not client.login:
        return "You are not logged"

    result = []
    chats = client.get_chats()
    for chat in chats:
        name = client.get_name(chat)
        if name is not None:
            result.append(name)
        else:
            result.append(chat)
    return result


class ServerNodeModel(BaseModel):
    id: int
    ip: str

@service.post("/ReceiveMessage")
def receive_message(nickname_from: str, nickname_to: str, value: str, request: Request):
    client: ClientInstance = request.state.client
    client.add_messages(nickname_from, nickname_to, value, -1)


@service.put("/register-server")
def register_server(model: ServerNodeModel, request: Request):
    client: ClientInstance = request.state.client
    node = RemoteIdentityNode(model.id, model.ip, SERVER_PORT)
    client.manager.add_nodes(node)
