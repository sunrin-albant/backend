from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import schemes, database
from services.transaction_service import TransactionService

transaction_router = APIRouter()

# Dependency to get the DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")




@transaction_router.post("/{transaction_post_id}", response_model=schemes.Transaction)
async def submit_transaction(
    transaction_post_id: str, 
    transaction: schemes.TransactionCreate, 
    db: Session = Depends(get_db), 
    token: str = Depends(oauth2_scheme)
):
    service = TransactionService(db)
    user_id = await service.get_current_user_id(token, db)
    # transaction_post_id와 user_id를 트랜잭션에 추가
    transaction.transaction_post_id = transaction_post_id
    transaction.user_id = user_id

    # 트랜잭션 생성
    return service.create_transaction(transaction)

@transaction_router.get("/{transaction_id}", response_model=schemes.Transaction)
def read_transaction(transaction_id: str, db: Session = Depends(get_db)):
    service = TransactionService(db)
    db_transaction = service.get_transaction(transaction_id=transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction

@transaction_router.get("/", response_model=list[schemes.Transaction])
def read_transactions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    service = TransactionService(db)
    return service.get_transactions(skip=skip, limit=limit)

@transaction_router.delete("/{transaction_id}", response_model=schemes.Transaction)
def delete_transaction(transaction_id: str, db: Session = Depends(get_db)):
    service = TransactionService(db)
    db_transaction = service.delete_transaction(transaction_id=transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction

@transaction_router.put("/{transaction_id}", response_model=schemes.Transaction)
async def update_transaction_status(
    transaction_id: str,
    transaction_update: schemes.TransactionUpdate,  # JSON 본문으로 받기
    db: Session = Depends(get_db)
):
    service = TransactionService(db)
    updated_transaction = service.update_transaction_status(transaction_id, transaction_update)
    if not updated_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return updated_transaction

@transaction_router.delete("/{transaction_id}", response_model=dict)
async def delete_transaction(
    transaction_id: str,
    db: Session = Depends(get_db)
):
    service = TransactionService(db)
    deleted_transaction = service.delete_transaction(transaction_id)
    
    if not deleted_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    return {"detail": "Transaction deleted successfully"}
