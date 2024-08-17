from sqlalchemy.orm import Session
from model import Notification

class NotificationRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_notifications(self, user_id: str, notification_type: int):
        notifications = self.db.query(Notification).filter(Notification.user_id == user_id, Notification.type == notification_type).all()
        return notifications