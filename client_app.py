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
from ui import UI
from gui import ChatApp

from src.service.multicast.client import client_multicast_discovery
# from src.service.multicast.multicast_utils import client_multicast_discovery

import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


client_api.on_event("shutdown")(client.save_nodes)

def start_client():
    logging.info("entrando a start_client()") 
    # Inyectamos el cliente en las apps FastAPI
    inject_to_state(client_api, "client", client)
    inject_to_state(service, "client", client)

    nodes: list[RemoteIdentityNode] = []
    logging.info("supuestamente ya tengo los nodos") 

    # 1) Descubrir servidores mediante multicast
    logging.info("voy a descubrir servidores, entrando a client_multicast_discovery()") 
    ip_addresses = client_multicast_discovery(timeout=5)
    logging.info(f"ya tengo la ip: {ip_addresses}") 
    logging.info(f"voy aentrar al if")
    if len(ip_addresses):
        logging.info(f"entre al if !!!")
        first_ip = ip_addresses[0]
        logging.info(f"first_ip: {first_ip}") 
        first_node = RemoteIdentityNode(-1, first_ip, SERVER_PORT)
        fs=first_node.serialize()
        logging.info(f"first_node: {fs}") 
        try:
            capacity = first_node.network_capacity()
            logging.info(f"capacity: {capacity}") 
        except:
            logging.error(f"Error al obtener capacity del primer nodo: {e}")
            pass
        else:
            for ip_found in ip_addresses:
                node_id = generate_id(f"{ip_found}:{SERVER_PORT}", capacity)
                logging.info(f"node_id: {node_id}") 
                node_obj = RemoteIdentityNode(node_id, ip_found, SERVER_PORT)
                logging.info(f"node_obj: {node_obj}") 
                nodes.append(node_obj)

    # 2) Leer caché de servidores (si existe)
    logging.info(f"voy a leer la caché de servidores")
    try:
        with open(SERVER_ADDRESSES_CACHE_FILENAME, "r") as j:
            servers = json.load(j)
    except:
        servers = []
    else:
        for s in servers:
            base = BaseNodeModel(**s)
            rn = RemoteIdentityNode.from_base_model(base)
            nodes.append(rn)

    # Añadimos todos los nodos descubiertos al manager
    client.manager.add_nodes(*nodes)
    logging.info(f"ya tengo los nodos")

    if len(client.manager.get_nodes()) == 0:
        raise Exception("Unable to find a server to connect")

    # Levantamos el microservicio local en un hilo
    def _service_task():
        config = Config(service, host=get_ip(), port=int(SERVICE_PORT))
        server = Server(config)
        asyncio.run(server.serve())
    service_task = Thread(target=_service_task, daemon=True)

    # Hilo para actualizar la lista de servidores
    def update():
        time.sleep(1)
        client.update_servers()
    stabilize_task = Thread(target=update, daemon=True)

    # Levantamos el microservicio principal (client_api)
    config = Config(client_api, host=LOCAL_IP, port=int(CLIENT_PORT))
    server = Server(config)
    service_task.start()
    stabilize_task.start()

    def server_run():
        asyncio.run(server.serve())
    server_task = Thread(target=server_run, daemon=True)
    server_task.start()


    time.sleep(1)
    # root = tk.Tk()
    # ChatApp(root, LOCAL_IP, CLIENT_PORT)
    # root.mainloop()
    console_ui = UI(LOCAL_IP, CLIENT_PORT)
    console_ui.start()


start_client()


#     # 1) Descubrir servidores con multicast
#     ip_addresses = client_multicast_discovery(timeout=5, attempts=5)

#     # Si encontramos IPs, las convertimos en RemoteIdentityNode
#     if len(ip_addresses):
#         first_ip = ip_addresses[0]
#         first_node = RemoteIdentityNode(-1, first_ip, SERVER_PORT)
#         try:
#             capacity = first_node.network_capacity()
#         except:
#             pass
#         else:
#             for ip_found in ip_addresses:
#                 node_id = generate_id(f"{ip_found}:{SERVER_PORT}", capacity)
#                 node_obj = RemoteIdentityNode(node_id, ip_found, SERVER_PORT)
#                 nodes.append(node_obj)

#     # 2) Leemos direcciones de server_addresses_cache.json (si existen)
#     try:
#         with open(SERVER_ADDRESSES_CACHE_FILENAME, "r") as j:
#             servers = json.load(j)
#     except:
#         servers = []
#     else:
#         for s in servers:
#             base = BaseNodeModel(**s)
#             rn = RemoteIdentityNode.from_base_model(base)
#             nodes.append(rn)

#     # Añadimos todos los nodos descubiertos al manager
#     client.manager.add_nodes(*nodes)

#     # Si no hay nodos, error
#     if len(client.manager.get_nodes()) == 0:
#         raise Exception("Unable to find a server to connect")

#     # Levantamos el microservicio local (service) en un hilo
#     def _service_task():
#         config = Config(service, host=get_ip(), port=int(SERVICE_PORT))
#         server = Server(config)
#         asyncio.run(server.serve())
#     service_task = Thread(target=_service_task, daemon=True)

#     # Hilo para actualizar la lista de servidores
#     def update():
#         time.sleep(1)
#         client.update_servers()
#     stabilize_task = Thread(target=update, daemon=True)

#     # Levantamos el microservicio principal (client_api)
#     config = Config(client_api, host=LOCAL_IP, port=int(CLIENT_PORT))
#     server = Server(config)

#     service_task.start()
#     stabilize_task.start()

#     def server_run():
#         asyncio.run(server.serve())
#     server_task = Thread(target=server_run, daemon=True)
#     server_task.start()

#     time.sleep(1)

#     # Interfaz gráfica (Tkinter)
#     root = tk.Tk()
#     ChatApp(root, LOCAL_IP, CLIENT_PORT)
#     root.mainloop()


# start_client()






# client_api.on_event("shutdown")(client.save_nodes)

# def start_client():
#     inject_to_state(client_api, "client", client)
#     inject_to_state(service, "client", client)

#     nodes: list[RemoteIdentityNode] = []

#     ip_addresses = broadcast_task(
#         timeout=5, limit=10, message_count=5, from_client=True)
#     # ip_addresses = client_multicast_discovery(timeout=5, attempts=3)
#     if len(ip_addresses):
#         first = RemoteIdentityNode(-1, ip_addresses[0], SERVER_PORT)
#         try:
#             capacity = first.network_capacity()
#         except:
#             pass
#         else:
#             nodes.extend([RemoteIdentityNode(generate_id(
#                 f"{ip}:{SERVER_PORT}", capacity), ip, SERVER_PORT) for ip in ip_addresses])

#     try:
#         servers: list[dict] = []
#         with open(SERVER_ADDRESSES_CACHE_FILENAME, "r") as j:
#             servers = json.load(j)
#     except:
#         pass
#     else:
#         if len(servers):
#             nodes.extend([RemoteIdentityNode.from_base_model(
#                 BaseNodeModel(**n)) for n in servers])

#     client.manager.add_nodes(*nodes)

#     if len(client.manager.get_nodes()) == 0:
#         raise Exception(
#             "Unable to find a server to connect")

#     def _service_task():
#         config = Config(service, host=get_ip(), port=int(SERVICE_PORT))
#         server = Server(config)
#         asyncio.run(server.serve())
#     service_task = Thread(target=_service_task, daemon=True)

#     def update():
#         time.sleep(1)
#         client.update_servers()
#     stabilize_task = Thread(target=update, daemon=True)

#     config = Config(client_api, host=LOCAL_IP, port=int(CLIENT_PORT))
#     server = Server(config)

#     service_task.start()
#     stabilize_task.start()

#     def server_run():
#         asyncio.run(server.serve())
#     server_task = Thread(target=server_run, daemon=True)
#     server_task.start()

#     time.sleep(1)

#     # ui = UI(LOCAL_IP, CLIENT_PORT)
#     # ui.start()

#     root = tk.Tk()
#     ChatApp(root, LOCAL_IP, CLIENT_PORT)
#     root.mainloop()

# start_client()
