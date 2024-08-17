from uuid import uuid4
from sqlalchemy.orm import Session
import model, schemes

class TransactionRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_transaction(self, transaction: schemes.TransactionCreate):
        db_transaction = model.Transaction(**transaction.dict())
        self.db.add(db_transaction)
        self.db.commit()
        self.db.refresh(db_transaction)
        
        transaction_post = self.get_transaction_post(db_transaction.transaction_post_id)
        title = transaction_post.title
        title = self.truncate_string(title, 5)
        user = self.get_user(transaction.user_id)
        user_name = user.username
        notification = model.Notification(
            notification_id=str(uuid4()),
            transaction_id=db_transaction.transaction_id,
            user_id=db_transaction.user_id,
            type=1,  # 알림의 타입 설정 (예: 1 = 새로운 거래 알림)
            content=f"{user_name}님이 본인의 {title}게시물에 양식을 제출하였습니다."
        )
        self.db.add(notification)
        self.db.commit()
        
        return db_transaction

    def truncate_string(self, s : str, max : int):
        if len(s) > max:
            return s[:max - 3] + '...'
        return s
    
    def get_transaction(self, transaction_id: str):
        return self.db.query(model.Transaction).filter(model.Transaction.transaction_id == transaction_id).first()

    def get_transactions(self, skip: int = 0, limit: int = 10):
        return self.db.query(model.Transaction).offset(skip).limit(limit).all()

    def get_transaction_post(self, transaction_post_id: str):
        return self.db.query(model.TransactionPost).filter(model.TransactionPost.transaction_post_id == transaction_post_id).first()

    def get_user(self, user_id: str):
        return self.db.query(model.User).filter(model.User.user_id == user_id).first()
    def delete_transaction(self, transaction_id: str):
        db_transaction = self.db.query(model.Transaction).filter(model.Transaction.transaction_id == transaction_id).first()
        if db_transaction:
            self.db.delete(db_transaction)
            self.db.commit()
        return db_transaction
    
    
    def update_transaction_status(self, transaction_id: str, transaction_update: schemes.TransactionUpdate):
        transaction = self.get_transaction(transaction_id)
        if transaction:
            transaction.status = transaction_update.status
            self.db.commit()
            self.db.refresh(transaction)
        else:
            print('Transaction not found')
        
        transaction_post = self.get_transaction_post(transaction.transaction_post_id)
        title = transaction_post.title
        title = self.truncate_string(title, 5)
        if transaction_update.status == 2:
            notification = model.Notification(
                notification_id=str(uuid4()),
                transaction_id=transaction_id,
                user_id=transaction.user_id,
                type=2,  # 알림의 타입 설정 (예: 2 = 거래 완료 알림)
                content=f"{title}글에 제출한 내용이 채택되었습니다."
            )
            self.db.add(notification)
            self.db.commit()
        
        return transaction
    
    def delete_transaction(self, transaction_id: str):
        transaction = self.get_transaction(transaction_id)
        if not transaction:
            return None
        
        self.db.delete(transaction)
        self.db.commit()
        return transaction
