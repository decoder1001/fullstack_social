from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.util import deprecated
from starlette import status

from database import SessionLocal
from models import User

router = APIRouter(prefix="/auth", tags=["auth"])
pages_router = APIRouter(tags=["pages"])
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
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    """
    Creates a new user with a hashed password and stores it in the database
    """
    create_user_model = User(
        username=create_user_request.username,
        email=create_user_request.email,
        password_hash=bcrypt_context.hash(create_user_request.password)
    )
    db.add(create_user_model)
    db.commit()
    #db.refresh(create_user_model)

def authenticate_user(username: str, password: str, db):
    """
    Verifies the username and password against stored hashed password.
    Returns the user if authentication is successful, otherwise returns False.
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password_hash):
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

def get_current_user(request: Request):
    """
    Decodes the JWT token and retrieves user details.
    Raises an exception if the token invalid or expired.
    """
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username, user_id = payload.get("sub"), payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(
                    status_code=401, detail="Could not validate user")
        return {"username": username, "id": user_id}

    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate User")

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    """
    Authenticates user credentials and returns a JWT token if valid.
    """
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(
                status_code=401, detail="Could not validate User"
        )
# BUG: First time logging in get an Unauthorized error
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    resp = JSONResponse({"access_token": token, "token_type": "bearer"})
    resp.set_cookie(key="access_token", value=token, httponly=True, samesite="lax", max_age=1200)
    return resp
