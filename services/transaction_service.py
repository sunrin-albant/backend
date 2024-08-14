import os
from dotenv import load_dotenv
from fastapi import HTTPException
import jwt
from sqlalchemy.orm import Session
import schemes
from repositories.transaction_repository import TransactionRepository

load_dotenv()

class TransactionService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = TransactionRepository(db)
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.ALGORITHM = os.getenv("ALGORITHM")

    def create_transaction(self, transaction: schemes.TransactionCreate) -> schemes.Transaction:
        return self.repository.create_transaction(transaction)

    def get_transaction(self, transaction_id: str):
        return self.repository.get_transaction(transaction_id)

    def get_transactions(self, skip: int = 0, limit: int = 10):
        return self.repository.get_transactions(skip, limit)
    
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
    
    def update_transaction_status(self, transaction_id: str, transaction_update: schemes.TransactionUpdate):
        return self.repository.update_transaction_status(transaction_id, transaction_update)
    
    def delete_transaction(self, transaction_id: str):
        return self.repository.delete_transaction(transaction_id)
