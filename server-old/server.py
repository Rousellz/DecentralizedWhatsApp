from flask import Flask, request, session, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "tu_clave_secreta"  # Cambia esto por una clave secreta aleatoria

DATABASE = "database.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Para acceder a las columnas por nombre
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Crear tabla de usuarios
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nickname TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """
    )
    # Crear tabla de contactos
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            contact_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(contact_id) REFERENCES users(id)
        )
    """
    )
    # Crear tabla de mensajes
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(sender_id) REFERENCES users(id),
            FOREIGN KEY(receiver_id) REFERENCES users(id)
        )
    """
    )
    conn.commit()
    conn.close()


init_db()


@app.route("/Register", methods=["POST"])
def register():
    nickname = request.args.get("nickname")
    password = request.args.get("password")
    if not nickname or not password:
        return "Nickname y contraseña requeridos", 400
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (nickname, password) VALUES (?, ?)", (nickname, password)
        )
        conn.commit()
        conn.close()
        return "Usuario registrado exitosamente", 200
    except sqlite3.IntegrityError:
        conn.close()
        return "El nickname ya existe", 400


@app.route("/Login", methods=["POST"])
def login():
    nickname = request.args.get("nickname")
    password = request.args.get("password")
    if not nickname or not password:
        return "Nickname y contraseña requeridos", 400
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM users WHERE nickname = ?", (nickname,))
    user = cursor.fetchone()
    conn.close()
    if user and user["password"] == password:
        session["user_id"] = user["id"]
        return "Inicio de sesión exitoso", 200
    else:
        return "Nickname o contraseña incorrectos", 400


@app.route("/Logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    return "Cierre de sesión exitoso", 200


@app.route("/GetContacts", methods=["GET"])
def get_contacts():
    if "user_id" not in session:
        return "No autorizado", 401
    user_id = session["user_id"]
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT contacts.name, users.nickname FROM contacts
        JOIN users ON contacts.contact_id = users.id
        WHERE contacts.user_id = ?
    """,
        (user_id,),
    )
    contacts = cursor.fetchall()
    conn.close()
    contacts_list = [{"name": c["name"], "nickname": c["nickname"]} for c in contacts]
    return jsonify(contacts_list), 200


@app.route("/AddContacts", methods=["POST"])
def add_contact():
    if "user_id" not in session:
        return "No autorizado", 401
    name = request.args.get("name")
    nickname = request.args.get("nickname")
    if not name or not nickname:
        return "Nombre y nickname requeridos", 400
    conn = get_db_connection()
    cursor = conn.cursor()
    # Obtener el ID del contacto
    cursor.execute("SELECT id FROM users WHERE nickname = ?", (nickname,))
    contact_user = cursor.fetchone()
    if not contact_user:
        conn.close()
        return "Usuario no encontrado", 404
    # Verificar si el contacto ya existe
    cursor.execute(
        "SELECT id FROM contacts WHERE user_id = ? AND contact_id = ?",
        (session["user_id"], contact_user["id"]),
    )
    if cursor.fetchone():
        conn.close()
        return "El contacto ya existe", 400
    # Agregar contacto
    cursor.execute(
        "INSERT INTO contacts (user_id, contact_id, name) VALUES (?, ?, ?)",
        (session["user_id"], contact_user["id"], name),
    )
    conn.commit()
    conn.close()
    return "Contacto agregado exitosamente", 200


@app.route("/DeleteContacts", methods=["POST"])
def delete_contact():
    if "user_id" not in session:
        return "No autorizado", 401
    name = request.args.get("name")
    if not name:
        return "Nombre requerido", 400
    conn = get_db_connection()
    cursor = conn.cursor()
    # Encontrar el contacto
    cursor.execute(
        "SELECT id FROM contacts WHERE user_id = ? AND name = ?",
        (session["user_id"], name),
    )
    contact = cursor.fetchone()
    if not contact:
        conn.close()
        return "Contacto no encontrado", 404
    cursor.execute("DELETE FROM contacts WHERE id = ?", (contact["id"],))
    conn.commit()
    conn.close()
    return "Contacto eliminado exitosamente", 200


@app.route("/GetChats", methods=["GET"])
def get_chats():
    if "user_id" not in session:
        return "No autorizado", 401
    user_id = session["user_id"]
    conn = get_db_connection()
    cursor = conn.cursor()
    # Obtener la lista de usuarios con los que ha chateado
    cursor.execute(
        """
        SELECT DISTINCT users.nickname FROM messages
        JOIN users ON (messages.sender_id = users.id OR messages.receiver_id = users.id)
        WHERE (messages.sender_id = ? OR messages.receiver_id = ?) AND users.id != ?
    """,
        (user_id, user_id, user_id),
    )
    chats = cursor.fetchall()
    conn.close()
    chats_list = [c["nickname"] for c in chats]
    return jsonify(chats_list), 200


@app.route("/SendMessage", methods=["POST"])
def send_message():
    if "user_id" not in session:
        return "No autorizado", 401
    user = request.args.get("user")
    message = request.args.get("message")
    if not user or not message:
        return "Usuario y mensaje requeridos", 400
    conn = get_db_connection()
    cursor = conn.cursor()
    # Obtener el ID del receptor
    cursor.execute("SELECT id FROM users WHERE nickname = ?", (user,))
    receiver = cursor.fetchone()
    if not receiver:
        conn.close()
        return "Usuario no encontrado", 404
    # Insertar mensaje
    cursor.execute(
        "INSERT INTO messages (sender_id, receiver_id, message) VALUES (?, ?, ?)",
        (session["user_id"], receiver["id"], message),
    )
    conn.commit()
    conn.close()
    return "Mensaje enviado", 200


@app.route("/GetMessages", methods=["GET"])
def get_messages():
    if "user_id" not in session:
        return "No autorizado", 401
    nickname = request.args.get("nickname")
    if not nickname:
        return "Nickname requerido", 400
    conn = get_db_connection()
    cursor = conn.cursor()
    # Obtener el ID del contacto
    cursor.execute("SELECT id FROM users WHERE nickname = ?", (nickname,))
    contact_user = cursor.fetchone()
    if not contact_user:
        conn.close()
        return "Usuario no encontrado", 404
    # Obtener mensajes entre el usuario actual y el contacto
    cursor.execute(
        """
        SELECT sender_id, message, timestamp FROM messages
        WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?)
        ORDER BY timestamp ASC
    """,
        (
            session["user_id"],
            contact_user["id"],
            contact_user["id"],
            session["user_id"],
        ),
    )
    messages = cursor.fetchall()
    conn.close()
    messages_list = []
    for m in messages:
        sender = "Tú" if m["sender_id"] == session["user_id"] else nickname
        messages_list.append(
            {"sender": sender, "message": m["message"], "timestamp": m["timestamp"]}
        )
    return jsonify(messages_list), 200


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
