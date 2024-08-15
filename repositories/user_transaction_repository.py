# repositories/user_transaction_repository.py
from sqlalchemy.orm import Session
from model import UserTransaction

class UserTransactionRepository:
    def __init__(self, db: Session):
        self.db = db
    
    
    def create_user_transaction(self, user_transaction: UserTransaction):
        self.db.add(user_transaction)
        self.db.commit()
        self.db.refresh(user_transaction)
        return user_transaction
    
    def get_user_transaction(self, user_transaction_post_id: str):
        return self.db.query(UserTransaction).filter(UserTransaction.user_transaction_post_id == user_transaction_post_id).first()
    
    def get_all_user_transactions(self):
        return self.db.query(UserTransaction).all()
    
    def update_user_transaction(self, user_transaction_post_id: str, heart: bool):
        user_transaction = self.get_user_transaction(user_transaction_post_id)
        if user_transaction:
            user_transaction.heart = heart
            self.db.commit()
            self.db.refresh(user_transaction)
        return user_transaction
    
    def delete_user_transaction(self,user_transaction_post_id: str):
        user_transaction = self.get_user_transaction(user_transaction_post_id)
        if user_transaction:
            self.db.delete(user_transaction)
            self.db.commit()
        return user_transaction
