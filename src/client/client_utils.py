from database.data_client import DataBaseClient
from src.server.identity.base_identity_node import BaseIdentityNode

SERVER_ADDRESSES_CACHE_FILENAME = "server_addresses_cache.json"

def task_receive_message(nickname: str, data: DataBaseClient, server_node_data: BaseIdentityNode):
    messages = server_node_data.search_messages_to(nickname, -1)
    server_node_data.delete_messages_to(nickname, -1)
    for message in messages:
        data.add_messages(message[0], nickname, message[1])

def register_user(node_inf: BaseIdentityNode, nickname: str, password: str, ip: str, port: str):
    try:
        result = node_inf.add_user(nickname, password, ip, port, -1)
        return result
    except:
        return False


def get_identity_data(node_inf: BaseIdentityNode):
    try:
        dict_successor = node_inf.successor()
        if dict_successor is not None:
            dict_successor_successor = dict_successor.successor()
            if dict_successor_successor is not None:
                return node_inf, dict_successor, dict_successor_successor
            return node_inf, dict_successor, None
        return node_inf, None, None
    except:
        return False, False, False


def add_message(node_inf: BaseIdentityNode, source: str, destiny: str, message: str):
    try:
        node_inf.add_messages(source, destiny, message, -1, -1)
    except:
        return False
