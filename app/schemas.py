from pydantic import BaseModel
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(PostBase):
    pass
class UpdatePost(BaseModel):
    published: bool

class post(BaseModel):
    title: str
    content: str
    published: bool
    created_at: datetime
    class Config:
        orm_mode = True