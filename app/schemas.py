from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import UUID4, BaseModel, EmailStr, root_validator


## USER
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    # created_at: datetime


class UserCreate(UserBase):
    password: str
    is_active: bool = True
    created_at: datetime = datetime.now()


class UserUpdate(UserBase):
    role: Optional[str] = "user"

    class Config:
        validate_assignment = True

    @root_validator
    def number_validator(cls, values):
        values["updated_at"] = datetime.now()
        return values


# use as response model
class UserOut(UserBase):
    id: UUID

    class Config:
        orm_mode = True


class UserIn(UserBase):
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


## POST
class PostBase(BaseModel):
    title: str
    content: str
    is_publish: bool = False
    tags: Optional[List[str]]


class PostCreate(PostBase):
    # user_id: str = UUID4 -- there's no need to add user_id manually because we get the id from the current_user
    created_at: datetime = datetime.now()


class PostUpdate(PostBase):
    # user_id: str = UUID4-- there's no need to add user_id manually because we get the id from the current_user

    class Config:
        validate_assignment = True

    @root_validator
    def number_validator(cls, values):
        values["updated_at"] = datetime.now()
        return values


# use as response model
class Post(PostBase):
    user_id: UUID4
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime]
    user: UserOut
    tags: Optional[List[str]]

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    data: List[Post]
    skip: int
    limit: int
    total: int

    class Config:
        orm_mode = True


## LOGIN
class Login(BaseModel):
    email: str
    password: str


## TOKEN
class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    id: UUID
    role: Optional[str]


class CurrentUser(BaseModel):
    id: UUID
    role: Optional[str]


class TokenPayload(BaseModel):
    user_id: UUID
