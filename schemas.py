from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class Book (BaseModel):
    title: str
    author: str
    review: str
    published: bool = True
    # created_at: datetime


class UserCreate (BaseModel):
    email: EmailStr
    password: str


class UserOut (BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]
