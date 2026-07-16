from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
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
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
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

def authenticate_user(username: str, password: str, db):
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

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    """
    Decodes the JWT token and retrieves user details.
    Raises an exception if the token invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithm=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: str = payload.get("id")
        if username is None or user_id is None:
            raise HTTPExeception(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate user"
            )

        return {"username": username, "id": user_id}

    except JWTError:
        raise HTTPExeception(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate User"
        )

@router.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    """
    Authenticates user credentials and returns a JWT token if valid.
    """
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPExeception(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate User"
        )
    username = user.username
    user_id = user.id
    token = create_access_token(username, user_id, timedelta(minutes=20))

    return {"access_token": token, "token_type": "bearer"}
