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
from src.service.broadcast.client import client_broadcast_task
from src.service.broadcast.server import broadcast_task

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

    capacity = min(capacity, 32)

    ip = get_ip(local)
    node = Node.create_network(ip, SERVER_PORT, capacity)

    inject_node(fastapi_app, node)

    healthy_task = threading.Thread(
        target=node.keep_healthy, args=(interval, node.update_replications), daemon=True)

    config = Config(fastapi_app, host=ip, port=int(SERVER_PORT))
    server = Server(config)

    healthy_task.start()
    client_broadcast_task()
    asyncio.run(server.serve())

@typer_app.command()
def other_server(local: bool = False, interval: float = 1):

    ip_addresses = broadcast_task(timeout=5, limit=1, message_count=5)
    if not len(ip_addresses):
        raise Exception(
            "Broadcast service failed: Unable to find a server node to connect")

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

    def join_network():
        time.sleep(1)
        node.join_network(remote_node)
        client_broadcast_task()
        node.keep_healthy(interval, node.update_replications)
    join_task = threading.Thread(target=join_network, daemon=True)

    config = Config(fastapi_app, host=ip, port=int(SERVER_PORT))
    server = Server(config)

    join_task.start()
    asyncio.run(server.serve())

typer_app()
