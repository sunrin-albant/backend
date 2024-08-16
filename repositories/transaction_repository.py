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
        
        notification = model.Notification(
            transaction_id=db_transaction.transaction_id,
            transaction_post_id=db_transaction.transaction_post_id,
            user_id=db_transaction.transaction_post.user_id,  # transaction_post의 user_id
            type=1,  # 알림의 타입 설정 (예: 1 = 새로운 거래 알림)
            content="새로운 거래가 생성되었습니다."
        )
        self.db.add(notification)
        self.db.commit()
        
        return db_transaction

    def get_transaction(self, transaction_id: str):
        return self.db.query(model.Transaction).filter(model.Transaction.transaction_id == transaction_id).first()

    def get_transactions(self, skip: int = 0, limit: int = 10):
        return self.db.query(model.Transaction).offset(skip).limit(limit).all()

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
            
        if transaction_update.status == 2:
            notification = model.Notification(
                transaction_id=transaction.transaction_id,
                transaction_post_id=transaction.transaction_post_id,
                user_id=transaction.user_id,  # transaction_post의 user_id
                type=2,  # 알림의 타입 설정 (예: 2 = 거래 완료 알림)
                content="거래가 완료되었습니다."
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
