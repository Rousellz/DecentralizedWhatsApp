from datetime import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class User(Base):
    __tablename__ = "user_account"

    nickname:  Mapped[str] = Column(
        String(30), unique=True, primary_key=True, nullable=False)
    password: Mapped[str] = Column(String(30), nullable=False)
    ip:        Mapped[str] = Column(String, nullable=False)
    port:      Mapped[str] = Column(String, nullable=False)

    def __repr__(self) -> str:
        return f"User(nickname={self.nickname!r},password={self.password!r},ip={self.ip!r},port={self.port!r})"


class Message(Base):
    __tablename__ = "messages"

    message_id: Mapped[int] = Column(Integer, primary_key=True)
    user_id_from: Mapped[int] = Column(ForeignKey("user_account.nickname"))
    user_id_to:   Mapped[int] = Column(ForeignKey("user_account.nickname"))
    value:        Mapped[str] = Column(String)

    def __repr__(self) -> str:
        return f"Message(id={self.message_id!r}, user_id_from={self.user_id_from!r}, user_id_to={self.user_id_to!r},value={self.value!r})"
