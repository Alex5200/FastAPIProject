from pydantic import BaseModel, Field, ConfigDict
from typing import List
from datetime import datetime


# Входные данные (Create)
class ChatCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)


class MessageCreate(BaseModel):
    chat_id: int  # FK int ✓
    text: str = Field(..., min_length=1, max_length=500)


# Выходные данные (Read)
class MessageRead(BaseModel):
    id: int
    chat_id: int
    text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChatRead(BaseModel):
    id: int
    title: str
    created_at: datetime
    messages: List[MessageRead] = []

    model_config = ConfigDict(from_attributes=True)
