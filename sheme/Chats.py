from uuid import uuid4
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Union

IdType = Union[str, int]

class Message(BaseModel):
    id: IdType = Field(default_factory=lambda: uuid4().hex)
    chat_id: IdType
    text: str = Field(..., min_length=1, max_length=500)
    createdAt: datetime

class Chat(BaseModel):
    id: IdType = Field(default_factory=lambda: uuid4().hex)
    title: str | None = Field(None, max_length=500)
    createdAt: datetime
    messages: List[Message] = []
