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
