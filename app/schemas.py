from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

from pydantic.types import conint

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str
    content: str
# default value set to True (making the field optional)
    published: bool = True
# optional field with default value of none or null
    rating: Optional[int] = 0

class PostCreate(PostBase):
    pass

#response schema/pydantic model
class Post(PostBase):
    id: int
#    title: str
#    content: str
#    published: bool
#    rating: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
# conditional integer only excepting a zero or a one
    dir: conint(ge=0, le=1)