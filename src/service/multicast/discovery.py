import socket
import struct
import time

import logging

from network_utils import get_ip
from network_utils.ip_address import IPAddress

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


MULTICAST_GROUP = "224.0.0.1"  # puedes cambiar esta dirección según tus necesidades
MULTICAST_PORT = 10000                # puerto para els descubrimiento multicast
DISCOVERY_MESSAGE = "DISCOVER_SERVERS"

def multicast_task(timeout=5, message_count=5):
    logging.info(f"entre a multicast_task")
    responses = []
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', MULTICAST_PORT))
    sock.settimeout(timeout)
    
    # Configurar TTL para limitar el alcance del multicast
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)

    # network_ip = IPAddress.from_string(ip) & NET_MASK
    # logging.info(f"network_ip: {network_ip}")
    # broadcast_ip = network_ip | (~NET_MASK)
    # logging.info(f"broadcast_ip: {broadcast_ip}")
    ip=get_ip()
    # Enviar varios mensajes de descubrimiento
    for _ in range(message_count):
        logging.info(f"enviando mensaje de descubrimiento")
        message= f"{DISCOVERY_MESSAGE},{ip}".encode()
        logging.info(f"{message}")
        sock.sendto(message, (MULTICAST_GROUP, MULTICAST_PORT))
        time.sleep(0.5)
    
    # Esperar respuestas
    start_time = time.time()
    while time.time() - start_time < timeout:
        logging.info(f"entre al while de multicast_task")
        try:
            logging.info("recibiendo respuesta")
            data, addr = sock.recvfrom(1024)
            logging.info(f"{data} {addr}")
            response, data_ip =data.decode().split(',')
            logging.info(f"response: {response}, data_ip: {data_ip}, addr: {addr[0]}, ip: {ip}")
            if response == DISCOVERY_MESSAGE and data_ip != ip:
                logging.info(f"response: {response}{data_ip}")
                responses.append(data_ip)
                logging.info(f"recibiendo respuesta de {data_ip}")
        except socket.timeout:
            break
    
    return list(set(responses))