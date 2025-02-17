from typing import Union
from ..chord.base_node import BaseNode
from .models import DataBaseUserModel


class BaseIdentityNode(BaseNode):
    """Base class for an identity node in a network."""

    def successor(self) -> Union["BaseIdentityNode", None]:
        """Get the successor node of the current node.

        Returns:
            Union[BaseIdentityNode, None]: The successor node if it exists, None otherwise.
        """
        raise NotImplementedError()

    def predecessor(self) -> Union["BaseIdentityNode", None]:
        """Get the predecessor node of the current node.

        Returns:
            Union[BaseIdentityNode, None]: The predecessor node if it exists, None otherwise.
        """
        raise NotImplementedError()

    def find_successor(self, id: int) -> Union["BaseIdentityNode", None]:
        """Find the successor node for a given ID.

        Args:
            id (int): The ID to search for.

        Returns:
            Union[BaseIdentityNode, None]: The successor node if found, None otherwise.
        """
        raise NotImplementedError()

    def get_users(self, database_id: int = -1) -> list[tuple[str, str, str, str]]:
        """Get the list of users in the node.

        Args:
            database_id (int, optional): The ID of the database. Defaults to -1.

        Returns:
            list[tuple[str, str, str, str]]: The list of users, each represented as a tuple of (nickname, password, IP, port).
        """
        raise NotImplementedError()

    def add_user(self, nickname: str, password: str, ip: str, port: str, database_id: int) -> bool:
        """Add a new user.

        Args:
            nickname (str): The nickname of the user.
            password (str): The password of the user.
            ip (str): The IP address of the user.
            port (str): The port number of the user.
            database_id (int): The ID of the database.

        Returns:
            bool: True if the user was added successfully, False otherwise.
        """
        raise NotImplementedError()

    def get_password(self, nickname: str, database_id: int) -> str:
        """Get the password of a user.

        Args:
            nickname (str): The nickname of the user.
            database_id (int): The ID of the database.

        Returns:
            str: The password of the user.
        """
        raise NotImplementedError()

    def delete_user(self, nickname: str, database_id: int) -> bool:
        """Delete a user.

        Args:
            nickname (str): The nickname of the user.
            database_id (int): The ID of the database.

        Returns:
            bool: True if the user was deleted successfully, False otherwise.
        """
        raise NotImplementedError()

    def update_user(self, nickname: str, ip: str, port: str, database_id: int) -> bool:
        """Update the IP and port of a user.

        Args:
            nickname (str): The nickname of the user.
            ip (str): The new IP address of the user.
            port (str): The new port number of the user.
            database_id (int): The ID of the database.

        Returns:
            bool: True if the user was updated successfully, False otherwise.
        """
        raise NotImplementedError()

    def get_ip_port(self, nickname: str, database_id: int) -> str:
        """Get the IP address and port number of a user.

        Args:
            nickname (str): The nickname of the user.
            database_id (int): The ID of the database.

        Returns:
            str: The IP address and port number of the user.
        """
        raise NotImplementedError()

    def nickname_identity_node(self, nickname: str, search_id: int = -1) -> Union["BaseIdentityNode", None]:
        """Get the node that corresponds to a given nickname.

        Args:
            nickname (str): The nickname to search for.
            search_id (int, optional): The ID to search for. Defaults to -1.

        Returns:
            Union[BaseIdentityNode, None]: The node that corresponds to the nickname if found, None otherwise.
        """
        raise NotImplementedError()

    def search_identity_node(self, nickname: str) -> Union["BaseIdentityNode", None]:
        """Search for the node that corresponds to a given nickname.

        Args:
            nickname (str): The nickname to search for.

        Returns:
            Union[BaseIdentityNode, None]: The node that corresponds to the nickname if found, None otherwise.
        """
        raise NotImplementedError()
  
    def add_messages(self, source: str, destiny: str, value: str, database_id: int, id: int) -> bool:
        """Add a message.

        Args:
            source (str): The source of the message.
            destiny (str): The destination of the message.
            value (str): The content of the message.
            database_id (int): The ID of the database.
            id (int): The ID of the message.

        Returns:
            bool: True if the message was added successfully, False otherwise.
        """
        raise NotImplementedError()

    def search_messages_to(self, me: str, database_id: int) -> list[tuple[str, str]]:
        """Search for messages addressed to a given user.

        Args:
            me (str): The nickname of the user.
            database_id (int): The ID of the database.

        Returns:
            list[tuple[str, str]]: The list of messages, each represented as a tuple of (source, value).
        """
        raise NotImplementedError()

    def delete_messages_to(self, me: str, database_id: int) -> bool:
        """Delete messages addressed to a given user.

        Args:
            me (str): The nickname of the user.
            database_id (int): The ID of the database.

        Returns:
            bool: True if the messages were deleted successfully, False otherwise.
        """
        raise NotImplementedError()

    def get_replication_data(self) -> DataBaseUserModel:
        """Get the replication data.

        Returns:
            DataBaseUserModel: The replication data.
        """
        raise NotImplementedError()

    def replicate(self, data: DataBaseUserModel, database_id: int) -> None:
        """Replicate the data.

        Args:
            data (DataBaseUserModel): The data to replicate.
            database_id (int): The ID of the database.
        """
        raise NotImplementedError()

    def all_nodes(self, search_id: int = -1) -> list["BaseIdentityNode"]:
        """Get all the nodes in the network.

        Args:
            search_id (int, optional): The ID to search for. Defaults to -1.

        Returns:
            list[BaseIdentityNode]: The list of all nodes in the network.
        """
        raise NotImplementedError()
