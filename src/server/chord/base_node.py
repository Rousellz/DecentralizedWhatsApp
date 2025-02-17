from pydantic import BaseModel
from typing import Union


class BaseNodeModel(BaseModel):
    id: int
    ip: str
    port: str


class BaseNode:
    """
    Represents a base node in a Chord network.

    Attributes:
        id (int): The unique identifier of the node.
        ip (str): The IP address of the node.
        port (str): The port number of the node.

    Methods:
        from_base_model(cls, model: BaseNodeModel): Creates a BaseNode instance from a BaseNodeModel object.
        from_serialized(cls, d: dict): Creates a BaseNode instance from a serialized dictionary.
        serialize(self): Serializes the BaseNode object into a dictionary.
        network_capacity(self) -> int: Returns the network capacity of the node.
        successor(self) -> Union["BaseNode", None]: Returns the successor node of the current node.
        set_successor(self, node: "BaseNode") -> None: Sets the successor node of the current node.
        predecessor(self) -> Union["BaseNode", None]: Returns the predecessor node of the current node.
        set_predecessor(self, node: "BaseNode") -> None: Sets the predecessor node of the current node.
        closest_preceding_finger(self, id: int) -> Union["BaseNode", None]: Returns the closest preceding finger node for a given identifier.
        find_successor(self, id: int) -> Union["BaseNode", None]: Finds the successor node for a given identifier.
        notify(self, node: "BaseNode") -> None: Notifies the current node about a new node in the network.
        heart(self) -> Union[str, None]: Performs a heart operation on the node.
        __repr__(self): Returns a string representation of the BaseNode object.
        __eq__(self, other: Union["BaseNode", None]): Checks if the current node is equal to another node.
        __hash__(self) -> int: Returns the hash value of the BaseNode object.
        __ne__(self, other: Union["BaseNode", None]): Checks if the current node is not equal to another node.
    """

    def __init__(self, id: int, ip: str, port: str):
        self.id = id
        self.ip = ip
        self.port = port

    @classmethod
    def from_base_model(cls, model: BaseNodeModel):
        """
        Creates a BaseNode instance from a BaseNodeModel object.

        Args:
            model (BaseNodeModel): The BaseNodeModel object.

        Returns:
            BaseNode: The created BaseNode instance.
        """
        return cls(model.id, model.ip, model.port)

    @classmethod
    def from_serialized(cls, d: dict):
        """
        Creates a BaseNode instance from a serialized dictionary.

        Args:
            d (dict): The serialized dictionary.

        Returns:
            BaseNode: The created BaseNode instance.
        """
        id = d.get("id", None)
        ip = d.get("ip", None)
        port = d.get("port", None)

        if id is not None and ip is not None and port is not None:
            return cls(id, ip, port)

    def serialize(self):
        """
        Serializes the BaseNode object into a dictionary.

        Returns:
            dict: The serialized dictionary.
        """
        return {"id": self.id, "ip": self.ip, "port": self.port}

    def network_capacity(self) -> int:
        """
        Returns the network capacity of the node.

        Returns:
            int: The network capacity.
        """
        raise NotImplementedError()

    def successor(self) -> Union["BaseNode", None]:
        """
        Returns the successor node of the current node.

        Returns:
            Union[BaseNode, None]: The successor node or None if it doesn't exist.
        """
        raise NotImplementedError()

    def set_successor(self, node: "BaseNode") -> None:
        """
        Sets the successor node of the current node.

        Args:
            node (BaseNode): The successor node.
        """
        raise NotImplementedError()

    def predecessor(self) -> Union["BaseNode", None]:
        """
        Returns the predecessor node of the current node.

        Returns:
            Union[BaseNode, None]: The predecessor node or None if it doesn't exist.
        """
        raise NotImplementedError()

    def set_predecessor(self, node: "BaseNode") -> None:
        """
        Sets the predecessor node of the current node.

        Args:
            node (BaseNode): The predecessor node.
        """
        raise NotImplementedError()

    def closest_preceding_finger(self, id: int) -> Union["BaseNode", None]:
        """
        Returns the closest preceding finger node for a given identifier.

        Args:
            id (int): The identifier.

        Returns:
            Union[BaseNode, None]: The closest preceding finger node or None if it doesn't exist.
        """
        raise NotImplementedError()

    def find_successor(self, id: int) -> Union["BaseNode", None]:
        """
        Finds the successor node for a given identifier.

        Args:
            id (int): The identifier.

        Returns:
            Union[BaseNode, None]: The successor node or None if it doesn't exist.
        """
        raise NotImplementedError()

    def notify(self, node: "BaseNode") -> None:
        """
        Notifies the current node about a new node in the network.

        Args:
            node (BaseNode): The new node.
        """
        raise NotImplementedError()

    def heart(self) -> Union[str, None]:
        """
        Performs a heart operation on the node.

        Returns:
            Union[str, None]: The result of the heart operation or None if it fails.
        """
        raise NotImplementedError()

    def __repr__(self):
        return f"{self.__class__.__name__}(id: {self.id})"

    def __eq__(self, other: Union["BaseNode", None]):
        """
        Checks if the current node is equal to another node.

        Args:
            other (Union[BaseNode, None]): The other node.

        Returns:
            bool: True if the nodes are equal, False otherwise.
        """
        if not other:
            return False

        return self.id == other.id and self.ip == other.ip and self.port == other.port
    
    def __hash__(self) -> int:
        """
        Returns the hash value of the BaseNode object.

        Returns:
            int: The hash value.
        """
        return self.id

    def __ne__(self, other: Union["BaseNode", None]):
        """
        Checks if the current node is not equal to another node.

        Args:
            other (Union[BaseNode, None]): The other node.

        Returns:
            bool: True if the nodes are not equal, False otherwise.
        """
        return not self.__eq__(other)
