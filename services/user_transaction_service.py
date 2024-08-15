# services/user_transaction_service.py
import os
from dotenv import load_dotenv
from fastapi import HTTPException
import jwt
from sqlalchemy.orm import Session
from repositories.user_transaction_repository import UserTransactionRepository
from model import UserTransaction

load_dotenv()

class UserTransactionService:
    def __init__(self, db: Session):
        self.db = db
        self.user_transaction_repository = UserTransactionRepository(db)
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.ALGORITHM = os.getenv("ALGORITHM")
    
    def create_user_transaction(self, user_transaction: UserTransaction):
        return self.user_transaction_repository.create_user_transaction(user_transaction)
    
    def get_user_transaction(self, user_transaction_post_id: str):
        return self.user_transaction_repository.get_user_transaction(user_transaction_post_id)
    
    def get_all_user_transactions(self):
        return self.user_transaction_repository.get_all_user_transactions()
    
    def update_user_transaction(self, user_transaction_post_id: str, heart: bool):
        return self.user_transaction_repository.update_user_transaction(user_transaction_post_id, heart)
    
    def delete_user_transaction(self, user_transaction_post_id: str):
        return self.user_transaction_repository.delete_user_transaction(user_transaction_post_id)
    
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
