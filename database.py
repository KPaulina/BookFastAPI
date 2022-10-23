from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import environ
import os

env = environ.Env()
environ.Env.read_env()

USER = os.environ.get("USER")
PASSWORD = os.environ.get("PASSWORD")
HOST = os.environ.get("HOST")
DB = os.environ.get("DB")

SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{PASSWORD}@{HOST}/{DB}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
