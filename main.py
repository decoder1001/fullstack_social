#TODO:
# User account creation and authentication
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
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
from auth import get_current_user, router

class UserBase(BaseModel):
    username: str
    email: str
    password_hash: str

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
app.include_router(router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@app.get("/")
async def root():
    return {"message": "FastAPI + PostgreSQL are running!"}
