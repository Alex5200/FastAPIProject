# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.Chats import Base

DATABASE_URL = "sqlite:///./chatapp.db"

engine = create_engine(
    DATABASE_URL,

)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)
