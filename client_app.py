import json
from uvicorn import Config, Server
from threading import Thread
import time
import asyncio
import tkinter as tk
from src.client.client import client_api, client, service
from src.client.client_utils import SERVER_ADDRESSES_CACHE_FILENAME
from network_utils import LOCAL_IP, CLIENT_PORT, SERVICE_PORT, SERVER_PORT, inject_to_state, get_ip
from src.server.hasher import generate_id
from src.server.identity.remote_identity_node import RemoteIdentityNode
from src.server.chord.base_node import BaseNodeModel
from src.service.broadcast.server import broadcast_task

from src.service.multicast.discovery import multicast_task

from ui import UI
from gui import ChatApp


import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


client_api.on_event("shutdown")(client.save_nodes)

def start_client():
    inject_to_state(client_api, "client", client)
    inject_to_state(service, "client", client)

    nodes: list[RemoteIdentityNode] = []
    logging.info("voy a descubrir servidores, entrando a client_multicast_discovery()") 
    ip_addresses = multicast_task(timeout=5, message_count=5)
    # ip_addresses = broadcast_task(
    #     timeout=5, limit=10, message_count=5, from_client=True)
    logging.info(f"ya tengo la ip: {ip_addresses}") 
    if len(ip_addresses):
        logging.info(f"entre al if !!!")
        first = RemoteIdentityNode(-1, ip_addresses[0], SERVER_PORT)
        try:
            capacity = first.network_capacity()
            logging.info(f"capacity: {capacity}") 
        except:
            pass
        else:
            nodes.extend([RemoteIdentityNode(generate_id(
                f"{ip}:{SERVER_PORT}", capacity), ip, SERVER_PORT) for ip in ip_addresses])
            logging.info(f"nodos identidad") 
            
    logging.info(f"voy a leer la caché de servidores")
    try:
        servers: list[dict] = []
        with open(SERVER_ADDRESSES_CACHE_FILENAME, "r") as j:
            servers = json.load(j)
            print(json.dumps(servers, indent=2))
    except:
        pass
    else:
        if len(servers):
            nodes.extend([RemoteIdentityNode.from_base_model(
                BaseNodeModel(**n)) for n in servers])

    client.manager.add_nodes(*nodes)
    logging.info(f"ya tengo los nodos")

    if len(client.manager.get_nodes()) == 0:
        raise Exception(
            "Unable to find a server to connect")

    def _service_task():
        config = Config(service, host=get_ip(), port=int(SERVICE_PORT))
        server = Server(config)
        asyncio.run(server.serve())
    service_task = Thread(target=_service_task, daemon=True)

    def update():
        time.sleep(1)
        logging.info("Actualizando servidores...")
        client.update_servers()
    stabilize_task = Thread(target=update, daemon=True)

    config = Config(client_api, host=LOCAL_IP, port=int(CLIENT_PORT))
    server = Server(config)

    service_task.start()
    stabilize_task.start()

    def server_run():
        asyncio.run(server.serve())
    server_task = Thread(target=server_run, daemon=True)
    server_task.start()

    time.sleep(1)

    # ui = UI(LOCAL_IP, CLIENT_PORT)
    # ui.start()

    root = tk.Tk()
    ChatApp(root, LOCAL_IP, CLIENT_PORT)
    root.mainloop()

start_client()
