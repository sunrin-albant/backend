#model.py
import uuid
from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
from enum import Enum as PyEnum
from datetime import datetime, timezone
from uuid import uuid4

class DepartmentEnum(PyEnum):
    SOFTWARE = 1
    HACKING = 2
    CONTENT_DESIGN = 3
    IT_MANAGEMENT = 4

class User(Base):
    __tablename__ = 'user'
    user_id = Column(String(255), primary_key=True, index=True)
    username = Column(String(10), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    point = Column(Integer)
    profile_pathname = Column(String(255))
    password = Column(String(255), nullable=False)
    department = Column(Enum(DepartmentEnum), nullable=True) 
    year = Column(Integer)
    created_date = Column(DateTime, default=datetime.now(timezone.utc))
    modified_date = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    is_active = Column(Boolean, default=False)
    verification_code = Column(Integer, nullable=True)
    
    # 관계 정의
    transaction_posts = relationship("TransactionPost", back_populates="user")
    user_transactions = relationship("UserTransaction", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")
    notifications = relationship("Notification", back_populates="user")


class TransactionPost(Base):
    __tablename__ = 'transaction_post'
    transaction_post_id = Column(String(255), primary_key=True, index=True, default=lambda: str(uuid4()))
    user_id = Column(String(255), ForeignKey("user.user_id"), nullable=False)
    title = Column(String(500), nullable=False)
    content = Column(String(5000), nullable=False)
    deadline = Column(Date, nullable=True)
    point = Column(Integer, nullable=False)
    tag = Column(String(255), nullable=True)
    image_pathname = Column(String(255), nullable=True)
    created_date = Column(DateTime, default=datetime.now(timezone.utc))

    # 관계 정의
    user = relationship("User", back_populates="transaction_posts")
    transactions = relationship("Transaction", back_populates="transaction_post")
    user_transactions = relationship("UserTransaction", back_populates="transaction_post")
    # notifications = relationship("Notification", back_populates="transaction_post")
    
class Transaction(Base):
    __tablename__ = 'transaction'
    
    transaction_id = Column(String(255), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    transaction_post_id = Column(String(255), ForeignKey('transaction_post.transaction_post_id'))
    user_id = Column(String(255), ForeignKey('user.user_id'))
    status = Column(Integer)
    content = Column(String(500))
    image_pathname = Column(String(255))
    created_date = Column(DateTime, default=datetime.now(timezone.utc))
    
    # 관계 정의
    user = relationship("User", back_populates="transactions")
    transaction_post = relationship("TransactionPost", back_populates="transactions")
    notifications = relationship("Notification", back_populates="transaction")

class UserTransaction(Base):
    __tablename__ = 'user_transaction'
    
    user_transaction_post_id = Column(String(255), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(255), ForeignKey('user.user_id'))
    transaction_post_id = Column(String(255), ForeignKey('transaction_post.transaction_post_id'))
    heart = Column(Boolean, default=False)
    
    # 관계 정의
    user = relationship("User", back_populates="user_transactions")
    transaction_post = relationship("TransactionPost", back_populates="user_transactions")

class Notification(Base):
    __tablename__ = 'notification'
    
    notification_id = Column(String(255), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    transaction_id = Column(String(255), ForeignKey('transaction.transaction_id'), nullable=False)
    user_id = Column(String(255), ForeignKey('user.user_id'), nullable=False)
    type = Column(Integer)
    content = Column(String(500))
    
    
    # 관계 정의
    transaction = relationship("Transaction", back_populates="notifications")
    user = relationship("User", back_populates="notifications")


