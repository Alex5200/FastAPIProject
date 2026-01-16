from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(500), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, server_default=text('NOW()'))

    messages = relationship(
        "Message",
        back_populates="chat",
        cascade="all, delete-orphan",
        lazy='selectin'
    )


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(
        Integer,
        ForeignKey("chats.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    text = Column(String(500), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=text('NOW()'))

    chat = relationship("Chat", back_populates="messages")
