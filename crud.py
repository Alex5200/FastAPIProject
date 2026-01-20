# crud.py
from sqlalchemy.orm import Session
from model.Chats import Chat, Message
from scheme.Chats import ChatCreate, MessageCreate


def create_chat(db: Session, chat_in: ChatCreate) -> Chat:
    chat = Chat(title=chat_in.title)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat


def get_chat(db: Session, chat_id: int) -> Chat | None:
    return db.query(Chat).filter(Chat.id == chat_id).first()

def get_chats(db: Session, skip: int = 0, limit: int = 10) -> list[Chat]:
    return db.query(Chat).offset(skip).limit(limit).all()

def create_message(db: Session, chat_id: int, msg_in: MessageCreate) -> Message:
    msg = Message(chat_id=chat_id, text=msg_in.text)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


def get_message(db: Session, message_id: int) -> Message | None:
    return db.query(Message).filter(Message.id == message_id).first()

def delete_chat(db: Session, chat_id: int) -> None:
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if chat:
        db.delete(chat)
        db.commit()

def put_chat(db: Session, chat_id: int, chat_in: ChatCreate) -> Chat | None:
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if chat:
        chat.title = chat_in.title
        db.commit()
        db.refresh(chat)
    return chat