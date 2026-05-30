from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # verifica la conexión antes de usarla ✅
    pool_recycle=300,  # recicla conexiones cada 5 minutos
    pool_size=5,  # máximo 5 conexiones simultáneas
    max_overflow=2,  # 2 conexiones extra si se necesitan
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
