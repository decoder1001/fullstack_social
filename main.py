#TODO:
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
from contextlib import asynccontextmanager
from typing import Annotated, List
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import engine, Base, AsyncSessionLocal
from app.api.endpoints import users
from app.models.user import User 

class UserBase(BaseModel):
    username: str
    email: str
    password: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan, title="FullStack_Social")

app.include_router(users.router, prefix="/users", tags=["users"])

def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/")
async def root():
    return {"message": "FastAPI + PostgreSQL are running!"}

@app.post("/signup")
async def signup(user: UserBase, db: db_dependency):
    db_username = user.UserInfo(user_input=user.user_input)
    db.add(db_username)
    db.commit()
    db.refresh(db_username)
    return db_user
