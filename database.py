from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
#from config import settings

DATABASE_URL: str = "postgresql://ross:Badonkadonk56@localhost:5432/socialdb"
PROJECT_NAME: str = "Fullstack_Social"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()
