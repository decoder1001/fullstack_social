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
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import SQLModel, Field, Session, create_engine, select

class user_account(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(index=True)
    passwd: str

app = FastAPI()

@app.post("/create-account/")
async def Account_Creation():
    new_name = input()
    new_passwd = input()
    return
