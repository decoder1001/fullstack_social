from sqlalchemy import String, Integer, Column
from app.core.database import Base

class User(Base):
    __table__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, index=True)
    surname = Column(String, index=True)
    email = Column(String, unique=True, nullable=False)
    passwd = Column(String, unique=True, index=True, nullable=False)

