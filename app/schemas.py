from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True

class UserAuth(BaseModel):
    email: EmailStr
    password: str

class CreatePost(PostBase):
    pass
class UpdatePost(BaseModel):
    title: str
    content: str
    published: bool = True

class Post(PostBase):
    id: int
    owner_id: int
    created_at: datetime
    owner: UserOut
    class Config:
        from_attributes = True
class Token(BaseModel):
    access_token:str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # type: ignore
