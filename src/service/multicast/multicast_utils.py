import socket
import struct
import time
from network_utils import inject_to_state, get_ip


MULTICAST_GROUP = '224.0.0.1' 
MULTICAST_PORT = 10000 
DISCOVERY_MESSAGE = "DISCOVER_SERVER" 
RESPONSE_PREFIX = "SERVER_RESPONSE:"

def server_multicast_listener(buffer_size=1024): 
    print(f"[Multicast Listener] Entre")

    try: 
        """ Escucha mensajes de descubrimiento multicast y responde con la IP del servidor. 
        :param get_server_ip_func: función que retorna la IP del servidor. """ 
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # Permite reusar la dirección 
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Se une al puerto de descubrimiento en todas las interfaces 
        sock.bind(('', MULTICAST_PORT)) # Se une al grupo multicast en todas las interfaces 
        mreq = struct.pack("4sL", socket.inet_aton(MULTICAST_GROUP), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq) 
        print(f"[Multicast Listener] Escuchando en {MULTICAST_GROUP}:{MULTICAST_PORT}")

        while True:
            try:
                data, address = sock.recvfrom(buffer_size)
                message = data.decode('utf-8').strip()
                if message == DISCOVERY_MESSAGE:
                    server_ip = get_ip()
                    response = f"{RESPONSE_PREFIX}{server_ip}"
                    sock.sendto(response.encode('utf-8'), (MULTICAST_GROUP, MULTICAST_PORT))
                    print(f"[Multicast Listener] Respondió al grupo {MULTICAST_GROUP}: {MULTICAST_PORT} con {server_ip}")
            except Exception as e:
                print(f"[Multicast Listener] Error: {e}")

    except Exception as e: 
        import traceback
        print(f"[Multicast Listener] Error: {e}") 
        traceback.print_exc()
    

def client_multicast_discovery(timeout=5):
    """
    Envía un mensaje de descubrimiento multicast y espera respuestas.
    Retorna una lista de IPs de servidores descubiertos.
    """
    responses = []
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Permitir reutilizar la dirección (nuevo)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Enlazar el socket al puerto multicast para recibir respuestas (nuevo)
    sock.bind(('', MULTICAST_PORT))
    # Unirse al grupo multicast para poder recibir mensajes enviados al grupo (nuevo)
    mreq = struct.pack("4sl", socket.inet_aton(MULTICAST_GROUP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    # Configura timeout
    sock.settimeout(timeout)
    # Configurar el TTL para el envío (asegura que el mensaje no salga de la red local)
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    message = DISCOVERY_MESSAGE.encode('utf-8')
    sock.sendto(message, (MULTICAST_GROUP, MULTICAST_PORT))
    print(f"[Client Discovery] Mensaje de descubrimiento enviado a {MULTICAST_GROUP}:{MULTICAST_PORT}")

    start_time = time.time()
    print("[Client Discovery]voy a entrar al while {start_time}")
    while time.time() - start_time < timeout:
        print("[Client Discovery]entrando al while")
        try:
            print("[Client Discovery] Esperando respuesta...")
            data, addr = sock.recvfrom(1024)
            print(f"[Client Discovery] Datos recibidos de {addr}")
            response = data.decode('utf-8').strip()
            print(f"[Client Discovery] voy a entrar al if el mensaje es: {response}")
            if response.startswith(RESPONSE_PREFIX):
                print(f"[Client Discovery] entreee")
                server_ip = response[len(RESPONSE_PREFIX):]
                
                print(f"[Client Discovery] Recibió respuesta de {addr}: {server_ip}")
                if server_ip not in responses:
                    responses.append(server_ip)
        except socket.timeout:
            break
        except Exception as e:
            print(f"[Client Discovery] Error: {e}")
            break
    
    return responses
