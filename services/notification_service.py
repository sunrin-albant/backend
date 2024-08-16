from fastapi import HTTPException
import jwt
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from repositories.notification_repository import NotificationRepository


load_dotenv()

class NotificationService:
    def __init__(self, db: Session):
        self.db = db
        self.notification_repository = NotificationRepository(db)
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.ALGORITHM = os.getenv("ALGORITHM")
        
    def get_user_notifications(self, user_id: str):
        return self.notification_repository.get_user_notifications(user_id)
        
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