# pip install sqlalchemy alembic fastapi python-dotenv uvicorn python-multipart jinja2
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
load_dotenv()

Base = declarative_base()

#Tabela de usuario
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(150), unique=True, nullable=False)
    senha = Column(String(100), nullable=False)

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

session = sessionmaker()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
        