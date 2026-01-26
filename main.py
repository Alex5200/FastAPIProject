import time
import logging
from datetime import datetime

from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Request, status

from model.Chats import Base
from scheme.Chats import ChatCreate, MessageCreate, ChatRead, MessageRead
from database import get_db, create_tables
import crud

app = FastAPI()

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.utcnow()

    response = await call_next(request)

    end_time = datetime.utcnow()
    duration = (end_time - start_time).total_seconds() * 1000

    logger.warning(
        f"{request.method} {request.url.path} — "
        f"Status: {response.status_code} — "
        f"Duration: {duration:.2f} ms"
    )

    return response


@app.on_event("startup")
def startup():
    create_tables()


@app.get("/")
def defaultroute():
    return {"server alive"}

@app.post(
    "/chats",
    tags=["Chats "],
    description="Create new chat",
    response_model=ChatRead,
    status_code=status.HTTP_201_CREATED,
)
def create_chat(chat: ChatCreate, db: Session = Depends(get_db)):
    db_chat = crud.create_chat(db, chat)
    return db_chat


@app.get(
    "/chats",
    tags=["Chats "],
    response_model=list[ChatRead],
    status_code=status.HTTP_200_OK,
)
def read_chats(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_chats = crud.get_chats(db, skip=skip, limit=limit)
    if not db_chats:
        raise HTTPException(status_code=404, detail="Chat not found")
    return db_chats


@app.get(
    "/chats/{chat_id}",
    tags=["Chats "],
    response_model=ChatRead,
    status_code=status.HTTP_200_OK,
)
def get_chat(chat_id: int, db: Session = Depends(get_db), response: Request = None):
    db_chat = crud.get_chat(db, chat_id)
    if not db_chat:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=404, detail="Chat not found")
    return db_chat


@app.put(
    "/chats/{chat_id}",
    tags=["Chats "],
    response_model=ChatRead,
    status_code=status.HTTP_200_OK,
)
def put_chat(chat_id: int, chat: ChatCreate, db: Session = Depends(get_db)):
    db_chat = crud.put_chat(db, chat_id, chat)
    if not db_chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return db_chat


@app.post(
    "/chats/{chat_id}/messages/",
    tags=["Chats "],
    response_model=MessageRead,
    status_code=status.HTTP_201_CREATED,
)
def create_message(chat_id: int, message: MessageCreate, db: Session = Depends(get_db)):
    chat = crud.get_chat(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    db_message = crud.create_message(db, chat_id, message)
    return db_message


@app.delete("/chats/{chat_id}", tags=["Chats "], status_code=status.HTTP_204_NO_CONTENT)
def delete_chat(chat_id: int, db: Session = Depends(get_db)):
    chat = crud.delete_chat(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return HTTPException(status_code=204, detail="No Content")
