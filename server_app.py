import asyncio
import threading
import time
from typer import Typer
from fastapi import FastAPI, Request
from uvicorn import Config, Server
from src.server.identity.identity_node import IdentityNode as Node
from src.server.identity.remote_identity_node import RemoteIdentityNode as RemoteNode
from src.server.hasher import generate_id
from src.server.chord.routers import router as chord_router
from src.server.identity.routers import router as identity_router
from network_utils import get_ip, LOCAL_IP, SERVER_PORT
# from src.service.broadcast.client import client_broadcast_task
# from src.service.broadcast.server import broadcast_task

from src.service.multicast.server import server_multicast_listener
from src.service.multicast.client import client_multicast_discovery

import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

def inject_node(app: FastAPI, node: Node):
    async def middleware(request: Request, call_next):
        request.state.node = node
        return await call_next(request)
    app.middleware("http")(middleware)

typer_app = Typer()

fastapi_app = FastAPI()
fastapi_app.include_router(chord_router)
fastapi_app.include_router(identity_router)

@typer_app.command() 
def first_server(capacity: int = 32, local: bool = False, interval: float = 1): 
    print('ggg')
    logging.info("Arrancando el primer servidor (nodo del anilloss)...")
    """ Arranca el primer servidor (nodo del anillo) y lanza un hilo 
    para responder a descubrimientos multicast. """ 
    capacity = min(capacity, 32) 
    ip = get_ip(local) 
    node = Node.create_network(ip, SERVER_PORT, capacity) 
    inject_node(fastapi_app, node)
    # Iniciar hilo de listener multicast. Se usa una lambda para obtener la IP actual.
    logging.info("Entrando a hilo multicast...")
    multicast_thread = threading.Thread(target=server_multicast_listener, args=(), daemon=True)
    multicast_thread.start()
    print("[Multicast] Hilo multicast iniciado.")

    # Hilo para mantener el nodo saludable
    healthy_task = threading.Thread(
        target=node.keep_healthy, args=(interval, node.update_replications), daemon=True
    )

    config = Config(fastapi_app, host=ip, port=int(SERVER_PORT))
    server = Server(config)
    healthy_task.start()
    try:
        asyncio.run(server.serve())
    except Exception as e:
        logging.error(f"Error en serve(): {e}") 
    # asyncio.run(server.serve())

@typer_app.command() 
def other_server(local: bool = False, interval: float = 1): 
    """ Arranca un servidor adicional. Usa multicast para descubrir 
    el primer servidor. """ # Se utiliza la función de descubrimiento multicast (por ejemplo, si se requiere en este caso) 
    ip_addresses = client_multicast_discovery(timeout=5, message=b"MESSAGE_FROM_SERVER") 
    if not ip_addresses: 
        raise Exception("Descubrimiento multicast falló: No se encontró ningún nodo servidor")
    
    remote_ip = ip_addresses[0]
    if local:
        remote_ip = LOCAL_IP

    remote_node = RemoteNode(-1, remote_ip, SERVER_PORT)
    capacity = remote_node.network_capacity()
    ip = get_ip(local)
    node = Node(ip, SERVER_PORT, capacity)
    remote_node.id = generate_id(f"{remote_ip}:{SERVER_PORT}", capacity)
    remote_node.set_local_node(node)
    inject_node(fastapi_app, node)

    # Se inicia también el hilo multicast para responder a nuevos descubrimientos
    multicast_thread = threading.Thread(target=server_multicast_listener, args=(), daemon=True)
    multicast_thread.start()

    def join_network():
        time.sleep(1)
        node.join_network(remote_node)
        node.keep_healthy(interval, node.update_replications)
    join_task = threading.Thread(target=join_network, daemon=True)

    config = Config(fastapi_app, host=ip, port=int(SERVER_PORT))
    server = Server(config)
    join_task.start()
    asyncio.run(server.serve())

typer_app()


# @typer_app.command()
# def first_server(capacity: int = 32, local: bool = False, interval: float = 1):

#     capacity = min(capacity, 32)

#     ip = get_ip(local)
#     node = Node.create_network(ip, SERVER_PORT, capacity)

#     inject_node(fastapi_app, node)

#     healthy_task = threading.Thread(
#         target=node.keep_healthy, args=(interval, node.update_replications), daemon=True)

#     config = Config(fastapi_app, host=ip, port=int(SERVER_PORT))
#     server = Server(config)

#     healthy_task.start()
#     client_broadcast_task()
#     asyncio.run(server.serve())

# @typer_app.command()
# def other_server(local: bool = False, interval: float = 1):

#     ip_addresses = broadcast_task(timeout=5, limit=1, message_count=5)
#     if not len(ip_addresses):
#         raise Exception(
#             "Broadcast service failed: Unable to find a server node to connect")

#     remote_ip = ip_addresses[0]

#     if local:
#         remote_ip = LOCAL_IP

#     remote_node = RemoteNode(-1, remote_ip, SERVER_PORT)

#     capacity = remote_node.network_capacity()

#     ip = get_ip(local)
#     node = Node(ip, SERVER_PORT, capacity)

#     remote_node.id = generate_id(f"{remote_ip}:{SERVER_PORT}", capacity)
#     remote_node.set_local_node(node)

#     inject_node(fastapi_app, node)

#     def join_network():
#         time.sleep(1)
#         node.join_network(remote_node)
#         client_broadcast_task()
#         node.keep_healthy(interval, node.update_replications)
#     join_task = threading.Thread(target=join_network, daemon=True)

#     config = Config(fastapi_app, host=ip, port=int(SERVER_PORT))
#     server = Server(config)

#     join_task.start()
#     asyncio.run(server.serve())

# typer_app()
