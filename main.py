# TODO:
# User account creation and authentication
#   1. Account creation
#   2. Account authentication
#   3. Account Dashboard (Show previous posts)
#   4. Friend request other users
# Post messages, images that remain presistant
#   1. Post messages
#       1.1. Message content
#       1.2. Message Timestamps
#   2. Post images
#   3. Have all posts remain presistant between shutdowns and resets
# Ability to like and comment on posts
#   1. Users can like posts
#   2. Users can comment on posts
#       2.2. Comment Timestamps
from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import SQLModel, Field, Session, create_engine, select
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

class user_account(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(index=True)
    passwd: str = Field(index=True)

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_db_and_table():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep - Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_table()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/create-account/")
def Account_Creation(user: User, session: SessionDep) -> User:
    new_name = input()
    new_passwd = input()
    return
