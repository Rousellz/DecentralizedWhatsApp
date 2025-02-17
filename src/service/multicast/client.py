import socket
import struct
import time

MCAST_GRP = "224.0.0.1"
MCAST_PORT = 10000

MESSAGE_FROM_CLIENT = b"MESSAGE_FROM_CLIENT"
MESSAGE_FROM_SERVER = b"MESSAGE_FROM_SERVER"
RESPONSE_PREFIX = "SERVER_RESPONSE:"

import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

def client_multicast_discovery(timeout=5, attempts=3,message=MESSAGE_FROM_CLIENT):
    logging.info(f"[Client Discovery] entrando a client_multicast_discovery()")
    """
    Envía 'MESSAGE_FROM_CLIENT' a 224.0.0.1:10000 'attempts' veces,
    luego escucha respuestas 'MESSAGE_FROM_SERVER'.
    Retorna la lista de IPs que hayan respondido.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    sock.bind(("", MCAST_PORT))

    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    sock.settimeout(timeout)

    found_nodes = []
    logging.info(f"[Client Discovery] Enviando mensaje de descubrimiento a {MCAST_GRP}:{MCAST_PORT} entrando al try")

    try:
        for _ in range(attempts):
            logging.info(f"[Client Discovery] entre al try voy a enviar el mensaje")
            sock.sendto(message, (MCAST_GRP, MCAST_PORT))
            time.sleep(0.2)
        logging.info(f"[Client Discovery] voy a entrar al while True para recibir")
        while True:
            try:
                data, addr = sock.recvfrom(1024)
                logging.info(f"[Client Discovery] voy a ver si el mensaje es correcto")
                response = data.decode('utf-8').strip()
                logging.info(f"[Client Discovery] voy a ver llego aqui? {data}, {response}")
                if response.startswith(RESPONSE_PREFIX):
                    print(f"[Client Discovery] entreee")
                    server_ip = response[len(RESPONSE_PREFIX):]
                    print(f"[Client Discovery] Recibió respuesta de {addr}: {server_ip}")
                    found_nodes.append(server_ip)
            except socket.timeout:
                break
    finally:
        sock.close()

    print(f"[Client Discovery] Los nodos descubienrtos {found_nodes}")
    found_nodes = list(set(found_nodes))
    return found_nodes