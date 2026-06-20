from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    first_name: str | None = None
    surname: str | None = None

class PostBase(BaseModel):
    content: str

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True

class CreatePost(PostBase):
    class Config:
        orm_mode = True
