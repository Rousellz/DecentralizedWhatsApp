import socket
import struct
import threading

import logging

from network_utils import get_ip

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


MULTICAST_GROUP = "224.0.0.1"  # misma que usas para el descubrimiento
MULTICAST_PORT = 10000          # mismo puerto para descubrimiento multicast
DISCOVERY_MESSAGE = "DISCOVER_SERVERS"

def multicast_listener(server_ip):
    logging.info("entrando a multicast_listener") 
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', MULTICAST_PORT))
    ip=get_ip()
    mreq = struct.pack('4sl', socket.inet_aton(MULTICAST_GROUP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
    
    while True:
        data, addr = sock.recvfrom(1024)
        logging.info(f"recibiendo multicast: {data} de {addr}")
        logging.info(f"encontre un mensaje")
        response, data_ip =data.decode().split(',')
        logging.info(f"response: {response}, data_ip: {data_ip}, addr: {addr[0]}, ip: {ip}")
        if response == DISCOVERY_MESSAGE and data_ip != ip :
            logging.info(f"entre al if de multicast_listener")
            # Envía la IP del servidor de respuesta
            message= f"{DISCOVERY_MESSAGE},{ip}".encode()
            logging.info(f"{message}")  
            sock.sendto(message, (MULTICAST_GROUP, MULTICAST_PORT))