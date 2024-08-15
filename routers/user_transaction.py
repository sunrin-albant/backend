# routers/user_transaction.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import database
from schemes import UserTransactionCreate, UserTransactionUpdate, UserTransactionResponse
from model import UserTransaction
from services.user_transaction_service import UserTransactionService

user_transaction_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@user_transaction_router.post("/", response_model=UserTransactionResponse)
async def create_user_transaction(
    user_transaction: UserTransactionCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    service = UserTransactionService(db)
    
    db_user_transaction = UserTransaction(
        user_id = await service.get_current_user_id(token, db), 
        transaction_post_id=user_transaction.transaction_post_id,
        heart=user_transaction.heart
    )
    return service.create_user_transaction(db_user_transaction)

@user_transaction_router.get("/{user_transaction_post_id}", response_model=UserTransactionResponse)
def get_user_transaction(user_transaction_post_id: str, db: Session = Depends(get_db)):
    service = UserTransactionService(db)
    db_user_transaction = service.get_user_transaction(user_transaction_post_id)
    if not db_user_transaction:
        raise HTTPException(status_code=404, detail="UserTransaction not found")
    return db_user_transaction

@user_transaction_router.put("/{user_transaction_post_id}", response_model=UserTransactionResponse)
def update_user_transaction(user_transaction_post_id: str, user_transaction: UserTransactionUpdate, db: Session = Depends(get_db)):
    service = UserTransactionService(db)
    updated_user_transaction = service.update_user_transaction(user_transaction_post_id, user_transaction.heart)
    if not updated_user_transaction:
        raise HTTPException(status_code=404, detail="UserTransaction not found")
    return updated_user_transaction

@user_transaction_router.delete("/{user_transaction_post_id}", response_model=UserTransactionResponse)
def delete_user_transaction(user_transaction_post_id: str, db: Session = Depends(get_db)):
    service = UserTransactionService(db)
    deleted_user_transaction = service.delete_user_transaction(user_transaction_post_id)
    if not deleted_user_transaction:
        raise HTTPException(status_code=404, detail="UserTransaction not found")
    return deleted_user_transaction