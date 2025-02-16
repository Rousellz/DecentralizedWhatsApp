from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Union
from .model_client import *

class DataBaseClient:
    """
    A class representing a database client.

    Attributes:
        session: The database session object.

    Methods:
        get_contacts: Retrieve contacts for a given nickname.
        add_contacts: Add a new contact.
        update_contact: Update the name of a contact.
        contain_contact: Check if a contact exists.
        delete_contact: Delete a contact.
        get_name: Get the name of a contact.
        get_nickname: Get the nickname of a contact.
        get_id: Get the ID of a contact.
        get_messages: Retrieve all messages.
        contain_messages: Check if a message exists.
        add_messages: Add a new message.
        delete_messages: Delete a message.
        search_messages_from: Search messages sent by a user.
        search_messages_to: Search messages received by a user.
        get_chats: Retrieve all chats for a given nickname.
        add_chat: Add a new chat.
        search_chat_id: Search the ID of a chat.
        delete_chat: Delete a chat.
        search_chat: Search messages in a chat.
    """

    def __init__(self, name: str = 'client_data'):
        engine = create_engine('sqlite:///'+name+'.sqlite',connect_args={"check_same_thread": False})
        session = sessionmaker(bind=engine)
        self.session = session()
        Base.metadata.create_all(engine)

    def get_contacts(self, mynickname: str) -> list[tuple[str, str]]:
        result = []
        try:
            contacts = self.session.query(Contacts).filter(
                Contacts.mynickname == mynickname , Contacts.name != "Unknown").all()
            for c in contacts:
                result.append((c.nickname, c.name))
            return result
        except:
            return result

    def add_contacts(self, mynickname_: str, nickname_: str, name_: str) -> bool:
        if self.contain_contact(mynickname_, nickname_):
            return False
        try:
            with self.session:
                contact = Contacts(
                    nickname=nickname_,
                    mynickname=mynickname_,
                    name=name_)
                self.session.add_all([contact])
                self.session.commit()
                return True
        except:
            return False

    def update_contact(self, mynickname: str, nickname: str, name: str) -> bool:
        try:
            self.session.query(Contacts).filter(
                Contacts.mynickname == mynickname , Contacts.nickname == nickname).update({Contacts.name: name})
            self.session.commit()
            return True
        except:
            return False

    def contain_contact(self, mynickname: str, nickname: str) -> bool:
        contain = self.session.query(Contacts).filter(Contacts.mynickname == mynickname, Contacts.nickname == nickname).first()
        return contain is not None

    def delete_contact(self, mynickname: str, nickname: str) -> bool:
        contain = self.session.query(Contacts).filter(
            Contacts.mynickname == mynickname , Contacts.nickname == nickname).first()
        if contain is not None:
            self.session.delete(contain)
            self.session.commit()
            return True
        return False

    def get_name(self, mynickname: str, nickname: str) -> Union[str,None]:
        try:
            name = self.session.query(Contacts).filter(
            Contacts.mynickname == mynickname , Contacts.nickname == nickname).one()
            return name.name
        except: 
            return None
    
    def get_nickname(self, mynickname: str, name: str) -> Union[str,None]:
        try:
            nickname = self.session.query(Contacts).filter(
            Contacts.mynickname == mynickname , Contacts.name == name).one()
            return nickname.nickname
        except:
            return None
        
    def get_id(self, mynickname: str, name: str) -> Union[str,None]:
        try:
            id = self.session.query(Contacts).filter(
            Contacts.mynickname == mynickname , Contacts.name == name).one()
            return id.id_contact
        except:
            return None
        
    def get_messages(self) -> list[tuple[int, str, str, str]]:
        result = []
        try:
            message = self.session.query(Message).all()
            for m in message:
                result.append((m.message_id,m.user_id_from,m.user_id_to,m.value))
            return result
        except:
            return result
    
    def contain_messages(self, id,source: str, destiny: str, value: str) -> bool:
        contain = self.session.query(Message).filter(Message.message_id==id, Message.user_id_from ==source, Message.user_id_to ==destiny,Message.value ==value ).first()
        return contain is not None


    def add_messages(self, source: str, destiny: str, value_: str, id: int = -1) -> bool:
        self.add_chat(source, destiny)
        id_chat = self.search_chat_id(source, destiny)
        try:
            with self.session:
                messages = Message(
                        user_id_from=source,
                        user_id_to=destiny,
                        chat_id=id_chat,
                        value=value_,)
                self.session.add_all([messages])
                self.session.commit()
                return True
        except:
            return False

    def delete_messages(self, id_message: int) -> bool:
        message = self.session.query(Message).get(id_message)
        if message is not None:
            self.session.delete(message)
            self.session.commit()
            return True
        return False

    def search_messages_from(self, me: str, user: str = '') -> list[tuple[str, str]]:
        result = []
        try:
            if user == ' ':
                query = self.session.query(Message).filter(
                    Message.user_id_from == me).all()
            else:
                query = self.session.query(Message).filter(
                    Message.user_id_from == me , Message.user_id_to == user).all()
            for q in query:
                result.append((q.user_id_from, q.value))
            return result
        except:
            return result
        
    def search_messages_to(self, me: str, user: str = ' ') -> list[tuple[str, str]]:
        result = []
        try:
            if user == ' ':
                query = self.session.query(Message).filter(
                    Message.user_id_to == me).all()
            else:
                query = self.session.query(Message).filter(
                    Message.user_id_from == user , Message.user_id_to == me).all()
            for q in query:
                result.append((q.user_id_from, q.value))

            return result
        except:
            return []

    def get_chats(self,mynickname:str)->list[str]:
        result = []
        chats1 = self.session.query(Chat).filter(Chat.user_id_1 == mynickname).all()
        chats2 = self.session.query(Chat).filter(Chat.user_id_2 == mynickname).all()
        for chat in chats1:
            result.append(chat.user_id_2)
        for chat in chats2:
            result.append(chat.user_id_1)    
        return result
    
    def add_chat(self, user_id_1_: str, user_id_2_: str) -> bool:
        if  self.search_chat_id(user_id_1_,user_id_2_) ==-1:
            try:
                with self.session:
                    chat = Chat(
                        user_id_1=user_id_1_,
                        user_id_2=user_id_2_,
                    )
                    self.session.add_all([chat])
                    self.session.commit()
                    return True
            except:
                return False
        return False
    
    def search_chat_id(self, user_id_1: str, user_id_2: str) -> int:
        try:
            chat = self.session.query(Chat).filter(
                Chat.user_id_1 == user_id_1, Chat.user_id_2 == user_id_2).one()
            return chat.chat_id
        except:
            try:
                chat = self.session.query(Chat).filter(
                    Chat.user_id_1 == user_id_2 , Chat.user_id_2 == user_id_1).one()
                return chat.chat_id
            except:
                return -1

    def delete_chat(self, user_id_1: str, user_id_2: str) -> bool:
        chat_id = self.search_chat_id(user_id_1, user_id_2)
        if chat_id is not False:
            for id in self.session.query(Message).filter(Message.chat_id == chat_id).all():
                self.session.delete(id)

            contain = self.session.query(Chat).get(chat_id)
            self.session.delete(contain)
            self.session.commit()
            return True
        return False

    def search_chat(self, user_id_1: str, user_id_2: str) -> list[tuple[str, str]]:
        chat_id = self.search_chat_id(user_id_1, user_id_2)
        result = []
        if chat_id != -1:
            query = self.session.query(Message).filter(
                Message.chat_id == chat_id).all()
            if query:
                for q in query:
                    result.append((q.user_id_from, q.value))
        return result
