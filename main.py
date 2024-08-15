#main.py
from fastapi import FastAPI
from database import SessionLocal, engine, database
from model import Base
from routers import transaction_router, register_router, transaction_posts_router, user_transaction_router

# 데이터베이스 테이블 생성 (필요한 경우)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# 데이터베이스 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# 라우터 등록
app.include_router(register_router, prefix="/register", tags=["register"])
app.include_router(transaction_posts_router, prefix="/transaction_posts", tags=["transaction_posts"])
app.include_router(transaction_router, prefix="/transactions", tags=["transactions"])
app.include_router(user_transaction_router, prefix="/user_transactions", tags=["user_transactions"])