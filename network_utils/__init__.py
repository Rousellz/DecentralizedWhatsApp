from fastapi import FastAPI, Request
import socket

LOCAL_IP = "127.0.0.1"
SERVICE_PORT = "8010"
SERVER_PORT = "8030"
CLIENT_PORT = "8070"
HEART_RESPONSE = "beat"

def get_ip(local=False):
    """
    Get the IP address of the current machine.

    Parameters:
    - local (bool): If True, returns the local IP address. If False, returns the public IP address.

    Returns:
    - ip (str): The IP address of the machine.
    """
    ip = ""

    if local:
        ip = LOCAL_IP
    else:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
        except:
            ip = LOCAL_IP

    return ip

def inject_to_state(app: FastAPI, name: str, obj):
    """
    Middleware function to inject an object into the state of the request.

    Args:
        app (FastAPI): The FastAPI application instance.
        name (str): The name of the attribute to be injected into the state.
        obj: The object to be injected into the state.

    Returns:
        Callable: The middleware function.

    """
    async def middleware(request: Request, call_next):
        setattr(request.state, name, obj)
        return await call_next(request)

    app.middleware("http")(middleware)
