from fastapi import HTTPException
import jwt
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
import model
from repositories.notification_repository import NotificationRepository


load_dotenv()

class NotificationService:
    def __init__(self, db: Session):
        self.db = db
        self.notification_repository = NotificationRepository(db)
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.ALGORITHM = os.getenv("ALGORITHM")
        
    def get_user_notifications_adopted(self, user_id: str, notification_type: int):
        return self.notification_repository.get_user_notifications(user_id, notification_type )
        
    async def get_current_user_id(self, token: str, db: Session):
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception
        except jwt.PyJWTError:
            raise credentials_exception
            # user = self.user_repository.get_user_by_id(db, user_id)
            # if user is None:
            #     raise credentials_exception
        return user_id
    
    def get_post_ids(self, user_id: str):
        posts = self.db.query(model.TransactionPost).filter(model.TransactionPost.user_id == user_id).all()
        post_ids = [post.transaction_post_id for post in posts]
        return post_ids
    
    def get_transactions(self, post_ids):
        transactions = self.db.query(model.Transaction).filter(model.Transaction.transaction_post_id.in_(post_ids)).all()
        transaction_ids = [transaction.transaction_id for transaction in transactions]
        return transaction_ids
    
    def get_user_notifications_submit(self, user_id: str, notification_type: int):
        post_ids = self.get_post_ids(user_id)
        transaction_ids = self.get_transactions(post_ids)
        notifications =  self.db.query(model.Notification).filter(model.Notification.type == notification_type, model.Notification.transaction_id.in_(transaction_ids)).all()
        return notifications