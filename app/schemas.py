from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True

class CreatePost(PostBase):
    pass
class UpdatePost(BaseModel):
    published: bool

class post(PostBase):
    created_at: datetime
    class Config:
        from_attributes = True
    
class UserCreate(BaseModel):
    email: EmailStr
    password: str