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
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
from auth import get_current_user, router, create_user

class UserBase(BaseModel):
    username: str
    email: str
    password_hash: str

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
app.include_router(router)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

def fake_decode_token(token):
    return UserBase(
            username=token + "fakedecoded", email="john@example.com", password_hash='fake543'
    )

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user

@app.get("/")
async def root():
    return {"message": "FastAPI + PostgreSQL are running!"}

@app.post("/signup")
async def signup(user: UserBase, db: db_dependency):
    create_user()
    

@app.get("/login", status_code=status.HTTP_200_OK)
async def login(user: user_dependency, db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return {"User": user} 

@app.get("/user/{user_id}") # FIX: Need to login to be authorized, must be authorized to login.
async def get_user(user_id: int, db: db_dependency):
    result = db.query(models.User).filter(models.User.id == user_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="User not found.")
    return result

@app.get("/users/me")
async def read_users_me(current_user: Annotated[UserBase, Depends(get_current_user)], db: db_dependency):
    return current_user
