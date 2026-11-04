from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPExeception, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Posts, User
from auth import get_current_user
from main import db_dependency, user_dependency

post_router APIRouter(prefix="/posts", tags=["posts"])

def get_db()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class PostRequest(BaseModel):
    content: str = Field(min_length=1, max_length=2000)

class PostResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
    author_username: str

    model_config = {"from_attributes": True}

@post_router.post("/home", status_code=status.HTTP_201_CREATED)
async def create_post(db: db_dependency, user: user_dependency, request: PostRequest):
    post = Posts(content=request.content, author=user["id"])
    db.add(post)
    db.commit()
    db.refresh(post)
    return {"id": post.id}

@post_router.get("/home")
async def list_posts(db: db_dependency):
    rows = (
        db.query(Posts, User.username)
        .join(User, Posts.author == User.id)
        .filter(Posts.published == True)
        .order_by(Posts.created_at.desc())
        .limit(50)
        .all()
    )
    return [
    {
        "id": p.id,
        "content": p.content,
        "created_at": p.created_at,
        "author_username": username,
    }
    for p, username in rows
]
