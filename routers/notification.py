from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import database
from schemes import Notification
from services.notification_service import NotificationService

notification_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@notification_router.get("/", response_model=List[Notification])
async def get_notifications(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    service = NotificationService(db)
    user_id = await service.get_current_user_id(token, db)
    notifications = service.get_user_notifications(user_id)
    if not notifications:
        raise HTTPException(status_code=404, detail="No notifications found")
    return notifications

# gpt 봐바 테이블 언어 utf-8로 바꿔야함
