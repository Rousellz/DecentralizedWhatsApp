import streamlit as st
import streamlit as st
import time
import traceback
import requests

# URL del servidor Flask
# SERVER_URL = "http://127.0.0.1:5000"
SERVER_URL = "http://10.0.11.10:5000"

if "session" not in st.session_state:
    st.session_state["session"] = requests.Session()

# Simulación de base de datos con diccionario en memoria
if "users" not in st.session_state:
    st.session_state["users"] = {}

if "logged_in_user" not in st.session_state:
    st.session_state["logged_in_user"] = None  # Usuario actualmente logueado

if "view" not in st.session_state:
    st.session_state["view"] = "login"  # Vista actual: login, home, contactos

def registrar_send(nickname, password):
    """
    Realiza una solicitud POST para registrar un usuario.
    :param nickname: El apodo del usuario (str).
    :param password: La contraseña del usuario (str).
    :return: Mensaje con el resultado de la operación.
    """
    # URL de destino (puedes reemplazarla con tu API real)
    url =f"{SERVER_URL}/Register"  # URL de prueba
    
    # Datos que se enviarán en la solicitud
    data = {
        "nickname": nickname,
        "password": password
    }

    try:
        # Realizar la solicitud POST
        response = st.session_state["session"].post(url, json=data,params=data)
        print(f"Se mando a {url} el mensaje con codigo {response.status_code}")
        # Comprobar el código de estado
        if response.status_code == 201:  # Creación exitosa
            return "Usuario registrado con éxito."
        elif response.status_code == 400:  # Error en los datos enviados
            return "Error: Solicitud incorrecta. Verifica los datos enviados."
        elif response.status_code == 409:  # Conflicto, usuario ya existe
            return "Error: El usuario ya está registrado."
        else:
            return f"Error desconocido. Código de estado: {response.status_code}"

    except requests.exceptions.RequestException as e:
        print(f"Error tipo {e} /n {traceback.format_exc()}")
        return f"Error al conectar con el servidor: {e}"

def login_send(nickname, password):
    """
    Realiza una solicitud POST para iniciar sesión de un usuario.
    :param nickname: El apodo del usuario (str).
    :param password: La contraseña del usuario (str).
    :return: Mensaje con el resultado de la operación.
    """
    # URL de destino (puedes reemplazarla con tu API real)
    url = f"{SERVER_URL}/Login"  # URL de prueba
    
    # Datos que se enviarán en la solicitud
    data = {
        "nickname": nickname,
        "password": password
    }

    try:
        response = st.session_state["session"].post(url, json=data, params=data)
        if response.status_code == 200:
            return {"success": True, "message": "Login exitoso"}
        elif response.status_code == 401:
            return {"success": False, "message": "Credenciales incorrectas"}
        elif response.status_code == 404:
            return {"success": False, "message": "Usuario no registrado"}
        else:
            return {"success": False, "message": f"Error desconocido: {response.status_code}"}
    except requests.RequestException as e:
        return {"success": False, "message": f"Error de conexión: {e}"}

def logout_send():
    """
    Realiza una solicitud POST para cerrar sesión del usuario.
    """
    url = f"{SERVER_URL}/Logout"
    
    try:
        # Usar la sesión persistente para enviar la solicitud
        response = st.session_state["session"].post(url)
        
        if response.status_code == 200:
            return {"success": True, "message": "Sesión cerrada con éxito."}
        else:
            return {"success": False, "message": f"Error desconocido: {response.status_code}"}
    except requests.RequestException as e:
        return {"success": False, "message": f"Error de conexión: {e}"}

def get_chats():
    """Obtiene la lista de chats del servidor para el usuario especificado."""
    url = f"{SERVER_URL}/GetChats"
    
    try:
        response = st.session_state["session"].get(url)
        # response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error al obtener los chats: {response.status_code} - {response.text}")
            return []
    except requests.RequestException as e:
        st.error(f"Error de conexión con el servidor: {e}")
        return []
# Función para obtener contactos del servidor
def get_contacts():
    """Obtiene los contactos del servidor para el usuario logueado."""
    url = f"{SERVER_URL}/GetContacts"
    
    try:
        response = st.session_state["session"].get(url)
        if response.status_code == 200:
            if response.json() :
                for contact in response.json() :
                    name = contact["name"]
                    nickname = contact["nickname"]

                    if st.button(name, key=f"chat_with_{name}"):
                        st.session_state["current_chat"] = nickname
                        st.session_state["view"] = "chat"
            else:
                st.write("No tienes contactos.")
        else:
            st.error(f"Error al obtener contactos: {response.status_code} - {response.text}")
            return []
    except requests.RequestException as e:
        st.error(f"Error de conexión con el servidor: {e}")
        return []
# Función para agregar contacto en el servidor
def add_contact(name, nickname):
    """Envía una solicitud para agregar un contacto."""
    url = f"{SERVER_URL}/AddContacts"
    data = {"name": name, "nickname": nickname}
    
    try:
        response = st.session_state["session"].post(url, params=data)
        if response.status_code == 200:
            st.success("Contacto agregado con éxito.")
        else:
            st.error(f"Error al agregar contacto: {response.status_code} - {response.text}")
    except requests.RequestException as e:
        st.error(f"Error de conexión al servidor: {e}")
# Función para eliminar contacto del servidor
def delete_contact(contact):
    """Envía una solicitud para eliminar un contacto."""
    url = f"{SERVER_URL}/DeleteContacts"
    
    try:
        response = st.session_state["session"].post(url, params={"name": contact})
        if response.status_code == 200:
            st.success("Contacto eliminado con éxito.")
        else:
            st.error(f"Error al eliminar contacto: {response.status_code} - {response.text}")
    except requests.RequestException as e:
        st.error(f"Error de conexión al servidor: {e}")

def get_messages(nickname):
    """Obtiene los mensajes de un chat."""
    url = f"{SERVER_URL}/GetMessages"
    try:
        response = st.session_state["session"].get(url, params={"nickname": nickname})
        if response.status_code == 200:
            return response.json()  # Devuelve la lista de mensajes
        else:
            st.error(f"Error al obtener mensajes: {response.status_code} - {response.text}")
            return []
    except requests.RequestException as e:
        st.error(f"Error de conexión al servidor: {e}")
        return []

def send_message(user, message):
    """Envía un mensaje a un usuario."""
    url = f"{SERVER_URL}/SendMessage"
    try:
        response = st.session_state["session"].post(url, params={"user": user, "message": message})
        if response.status_code == 200:
            return True
        else:
            st.error(f"Error al enviar mensaje: {response.status_code} - {response.text}")
            return False
    except requests.RequestException as e:
        st.error(f"Error de conexión al servidor: {e}")
        return False
# Función para la pestaña de registro
def register():
    st.title("Registro")
    
    username = st.text_input("Nombre de usuario a registrar")
    password = st.text_input("Contraseña a registrar", type="password")
    confirm_password = st.text_input("Confirmar Contraseña", type="password")
    
    if st.button("Registrar"):
        if not username or not password or not confirm_password:
            st.error("Por favor, completa todos los campos.")
        elif password != confirm_password:
            st.error("Las contraseñas no coinciden.")
        elif username in st.session_state["users"]:
            st.error("El nombre de usuario ya está registrado.")
        else:
            st.session_state["users"][username] = password
            st.success(f"Usuario {username} registrado con éxito. Ahora puedes iniciar sesión.")
            print(f"Registrando {username} con contraseña {password}")
            registrar_send(username,password)
            print("Usuario registrado")
# Función para la pestaña de login
def login(): 
    st.title("Iniciar Sesión")
    
    username = st.text_input("Nombre de usuario")
    password = st.text_input("Contraseña", type="password")
    
    if st.button("Iniciar Sesión"):

        result = login_send(username, password)
        if result["success"]:
            # st.success(result["message"])
            st.success(f"¡Bienvenido de nuevo, {username}!")
            st.session_state["logged_in_user"] = username
            st.session_state["view"] = "home"  # Cambiar a la vista de inicio
        else:
            st.error(result["message"])

def home_screen():
    st.title(f"Bienvenido, {st.session_state['logged_in_user']}")
    col1, col2 = st.columns(2)

    with col1:
        # Botón para ir a la pantalla de contactos
        if st.button("Contactos"):
            st.session_state["view"] = "contacts"  # Cambiar a la vista de contactos

    with col2:
        # Botón para cerrar sesión
        if st.button("Cerrar Sesión"):
        # Llamar al servidor para cerrar sesión
            logout_result = logout_send()
            if logout_result["success"]:
                st.success("Sesión cerrada con éxito.")
                st.session_state["logged_in_user"] = None
                st.session_state["view"] = "login"  # Cambiar a la vista de login
            else:
                st.error(f"Error al cerrar sesión: {logout_result['message']}")

    # Mostrar chats del usuario logueado
    st.subheader("Tus Chats")
    username = st.session_state["logged_in_user"]
    chats = get_chats()
    if chats:
        for chat in chats:
            if st.button(chat, key=f"chat_with_{chat}"):
                st.session_state["current_chat"] = chat
                st.session_state["view"] = "chat"
    else:
        st.write("No tienes chats aún.")

# Pantalla de contactos
def contacts_screen():
    username = st.session_state["logged_in_user"]

    col1, col2 = st.columns(2)

    with col1:
        with st.container():
            st.title("Contactos")
    with col2:
        with st.container():
            st.write("") 
            st.write("") 
            if st.button("Volver"):
                st.session_state["view"] = "home"  # Cambiar a la vista de inicio

    tab1, tab2, tab3 = st.tabs(["Contactos","Agregar", "Eliminar"])

    with tab2:
        # Botón para agregar contacto
        st.subheader("Agregar Contacto")
        name = st.text_input("Nombre del nuevo contacto", key="add_contact_name")
        nickname = st.text_input("Nickname del nuevo contacto", key="add_contact_nickname")
        if st.button("Agregar"):
            if not name or not nickname:
                st.error("Nombre y nickname son requeridos.")
            else:
                if add_contact(name, nickname):
                    st.success("Contacto agregado con éxito.")
                else:
                    st.warning("Por favor, ingresa un nombre válido.")
    with tab3:
        # Botón para eliminar contacto
        st.subheader("Eliminar Contacto")
        contact_to_remove = st.text_input("Nombre del contacto a eliminar", key="remove_contact")
        if st.button("Eliminar"):
            if contact_to_remove:
                delete_contact(contact_to_remove)
            else:
                st.warning("Por favor, ingresa un nombre válido.")
        # Botón para volver a la pantalla anterior
    with tab1:
        # Mostrar contactos actuales
        st.subheader("Tus Contactos")
        get_contacts()

def chat_screen():
    current_chat = st.session_state.get("current_chat", None)
    # Botón para volver a la lista de contactos
    if st.button("Volver a Contactos"):
        st.session_state["view"] = "contacts"

    st.title(f"Chat con {current_chat}")

    # Mostrar mensajes del chat
    messages = get_messages(current_chat)
    if messages:
        for msg in messages:
            sender = msg["sender"]
            message = msg["message"]
            timestamp = msg["timestamp"]
            st.markdown(f"`{timestamp}` **{sender}:** {message}")
    else:
        st.write("No hay mensajes en este chat.")


# Widget de entrada de mensaje
    if "message_sent" not in st.session_state:
        st.session_state["message_sent"] = False

    new_message = st.text_input(
        "Escribe tu mensaje:",
        key="new_message",
    )

    if st.button("Enviar") and not st.session_state["message_sent"]:
        st.session_state["message_sent"] = True
        if new_message.strip():
            if send_message(current_chat, new_message.strip()):
                st.success("Mensaje enviado.")
                # st.session_state["new_message"] = ""  # Limpiar el campo después de enviar
                # st.experimental_rerun()
            else:
                st.error("No se pudo enviar el mensaje.")
        st.session_state["message_sent"] = False  # Restablecer el estado del botón
    time.sleep(1)
    st.rerun()


# Controlador principal de vistas
if st.session_state["view"] == "login":
    # Configuración de las pestañas
    tab1, tab2 = st.tabs(["Registro", "Login"])

    with tab1:
        register()

    with tab2:
        login()

elif st.session_state["view"] == "home":
    home_screen()
elif st.session_state["view"] == "contacts":
    contacts_screen()
elif st.session_state["view"] == "chat":
    chat_screen()



