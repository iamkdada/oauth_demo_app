from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging

from src.schemas import User as UserSchema, UserCreate
from src.models import User, SessionLocal, init_db

# ログの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# データベースの初期化
init_db()


# データベースセッションの取得
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users/", response_model=List[UserSchema])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@app.get("/users/{user_id}", response_model=UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/users/", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
