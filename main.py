#TODO:
# User account creation and authentication
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
from typing import Annotated, List
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal

class UserBase(BaseModel):
    username: str
    email: str
    password_hash: str

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
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
    db_userinfo = models.User(username=user.username, email=user.email, password_hash=user.password_hash)
    db.add(db_userinfo)
    db.commit()
    db.refresh(db_userinfo)

@app.get("/user/{user_id}")
async def get_user(user_id: int, db: db_dependency):
    result = db.query(models.User).filter(models.User.id == user_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="User not found.")
    return result
