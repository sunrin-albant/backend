# transaction_post_repository.py

from sqlalchemy import or_
from sqlalchemy.orm import Session
from model import TransactionPost
from schemes import TransactionPostCreate, TransactionPostUpdate

class TransactionPostRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_post(self, post: TransactionPostCreate, user_id : str) -> TransactionPost:
        post_data = post.dict()
        post_data['user_id'] = user_id  # user_id를 딕셔너리에 추가
        db_post = TransactionPost(**post_data)
        self.db.add(db_post)
        self.db.commit()
        self.db.refresh(db_post)
        return db_post

    def get_post(self, post_id: str) -> TransactionPost:
        return self.db.query(TransactionPost).filter(TransactionPost.transaction_post_id == post_id).first()

    def update_post(self, post_id: str, post: TransactionPostUpdate) -> TransactionPost:
        db_post = self.get_post(post_id)
        if db_post:
            for key, value in post.dict(exclude_unset=True).items():
                setattr(db_post, key, value)
            self.db.commit()
            self.db.refresh(db_post)
        return db_post

    def delete_post(self, post_id: str) -> bool:
        db_post = self.get_post(post_id)
        if db_post:
            self.db.delete(db_post)
            self.db.commit()
            return True
        return False

    def get_all_posts(self) -> list[TransactionPost]:
        return self.db.query(TransactionPost).all()
    
    def search_posts(self, search: str):
        results = self.db.query(TransactionPost).filter(
            or_(
                TransactionPost.title.ilike(f"%{search}%"),  # title에서 검색 (대소문자 구분 없이)
                TransactionPost.tag.ilike(f"%{search}%"),
                TransactionPost.tag2.ilike(f"%{search}%") # tag에서 검색 (대소문자 구분 없이)
            )
        ).all()
        return results
    
    
