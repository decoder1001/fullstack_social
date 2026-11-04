#TODO:
# User account creation and authentication
#   3. Account Dashboard (Show previous posts)
# Post messages, images that remain presistant
#   1. Post messages
#       1.1. Message content
#       1.2. Message Timestamps
from typing import Annotated, List
from fastapi import FastAPI, HTTPException, Depends, status, Request, WebSocket, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
from auth import get_current_user, router, pages_router
from posts import Posts_router

class UserBase(BaseModel):
    username: str
    email: str
    password_hash: str

class PostBase(BaseModel):
    content: str

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount ("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
posts_router = APIRouter(prefix="/posts", tags=["posts"])

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )
 
@pages_router.get("/home", response_class=HTMLResponse)
async def user_homepage(user: user_dependency, request: Request):
    return templates.TemplateResponse(
        request, "userHome.html", {"username": user["username"]}
    )

@posts_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_post(db: db_dependency, request: PostRequest, user: user_dependency):
    post = Posts(content=request.content, author=user["id"])
    db.add(post)
    db.commit()
    db.commit(post)
    return {"id": post.id}

app.include_router(router)
app.include_router(pages_router)
app.include_router(posts_router)
