from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from model.Chats import Base
from scheme.Chats import ChatCreate, MessageCreate, ChatRead, MessageRead
from database import get_db, create_tables
import crud

app = FastAPI()


@app.on_event("startup")
def startup():
    create_tables()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/chats", response_model=ChatRead)
def create_chat(chat: ChatCreate, db: Session = Depends(get_db)):
    db_chat = crud.create_chat(db, chat)
    return db_chat


@app.get("/chats/{chat_id}", response_model=ChatRead)
def get_chat(chat_id: int, db: Session = Depends(get_db)):
    db_chat = crud.get_chat(db, chat_id)
    if not db_chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return db_chat


@app.post("/chats/{chat_id}/messages/", response_model=MessageRead)
def create_message(chat_id: int, message: MessageCreate, db: Session = Depends(get_db)):
    chat = crud.get_chat(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    db_message = crud.create_message(db, chat_id, message)
    return db_message


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.delete("/chats/{chat_id}")
def delete_chat(chat_id: int, db: Session = Depends(get_db)):
    chat = crud.delete_chat(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return HTTPException(status_code=204, detail="No Content")
