#schemes.py
from pydantic import BaseModel, EmailStr
from datetime import date, datetime

# 사용자 생성을 위한 스키마
class UserCreate(BaseModel):
    username: str
    password: str
    department: int | None = None
    year: int | None = None
    email: str | None = None
    profile_pathname: str | None = None

# 사용자 읽기를 위한 스키마
class UserOut(BaseModel):
    username: str
    password: str
    department: int | None = None
    year: int | None = None
    email: str | None = None
    profile_pathname: str | None = None

    class Config:
        orm_mode = True
        
class UserLogin(BaseModel):
    email: str
    password: str

class TransactionPostBase(BaseModel):
    user_id: str
    title: str
    content: str
    deadline: date | None = None
    point: int
    tag: str | None = None
    image_pathname: str | None = None

class TransactionPostCreate(TransactionPostBase):
    pass

class TransactionPostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    deadline: date | None = None
    point: int | None = None
    tag: str | None = None
    image_pathname: str | None = None

class TransactionPostOut(TransactionPostBase):
    transaction_post_id: str
    created_date: datetime

    class Config:
        orm_mode = True
        
    
class VerificationCodeModel(BaseModel):
    email: EmailStr
    code: int
    
class TransactionBase(BaseModel):
    status: int
    content: str | None = None
    image_pathname: str | None = None

class TransactionCreate(TransactionBase):
    transaction_post_id: str | None = None
    user_id: str | None = None

class Transaction(TransactionBase):
    transaction_id: str
    transaction_post_id: str
    user_id: str
    created_date: datetime

    class Config:
        orm_mode = True
        
class TransactionUpdate(BaseModel):
    status: int

    class Config:
        orm_mode = True
        
class UserTransactionCreate(BaseModel):
    user_id: str | None = None
    transaction_post_id: str
    heart: bool = False

class UserTransactionUpdate(BaseModel):
    heart: bool

class UserTransactionResponse(BaseModel):
    user_transaction_post_id: str
    user_id: str
    transaction_post_id: str
    heart: bool
    
    class Config:
        orm_mode = True
        
class Notification(BaseModel):
    notification_id: str
    transaction_id: str | None = None
    transaction_post_id: str | None = None
    user_id: str
    type: int
    content: str

    class Config:
        orm_mode = True