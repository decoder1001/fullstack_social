from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPExeception
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.util import deprecated
from starlette import status

from database import SessionLocal
from models import User

router = APIRouter(prefix="/auth", tags=["auth"])
SECRET_KEY = "5ed825e17bd774e1a962b0d354a75e4df14509016486656649bd7e94ba1ca3d6"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest)
    """
    Creates a new user with a hashed password and stores it in the database
    """
    create_user_model = Users(
        username=create_user_request.username,
        email=create_user_request.email,
        hashed_password=bcrypt_context.hash(create_user_request.password)
    )
    db.add(create_user_model)
    db.commit()

def authenticate_user(username: str, password: str, db)
    """
    Verifies the username and password against stored hashed password.
    Returns the user if authentication is successful, otherwise returns False.
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    """
    Generates a JWT access token with an expiration time.
    """
    encode = {"sub": username, "id": user_id}
    expires = datetime.now() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
