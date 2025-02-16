import socket
import struct
import time
import logging
from network_utils import inject_to_state, get_ip


# Configuración de logs
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

MCAST_GRP = "224.0.0.1"
MCAST_PORT = 10000

MESSAGE_FROM_CLIENT = b"MESSAGE_FROM_CLIENT"
MESSAGE_FROM_SERVER = b"MESSAGE_FROM_SERVER"
RESPONSE_PREFIX = "SERVER_RESPONSE:"

def server_multicast_listener():
    logging.info("[Multicast] Iniciando server_multicast_listener()...")
    """
    Bucle infinito: 
    - Se une a 224.0.0.1:10000
    - Cuando recibe MESSAGE_FROM_CLIENT, responde con MESSAGE_FROM_SERVER
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(("", MCAST_PORT))

    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    logging.info(f"[Multicast] Servidor escuchando en {MCAST_GRP}:{MCAST_PORT}...")

    while True:
        logging.info("[Multicast] Esperando mensajes...")
        data, addr = sock.recvfrom(1024)
        logging.info(f"[Multicast] Recibido: {data} de {addr}")
        if data == MESSAGE_FROM_CLIENT:
            # Respondemos con MESSAGE_FROM_SERVER
            server_ip = get_ip()
            response = f"{RESPONSE_PREFIX}{server_ip}"
            logging.info(f"[Multicast] Enviando respuesta a {addr} (al cliente){response}")
            sock.sendto(response.encode('utf-8'), (MCAST_GRP, MCAST_PORT))
            # sock.sendto(response, (MCAST_GRP, MCAST_PORT))
        time.sleep(0.1)
