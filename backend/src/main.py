from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List
from jose import JWTError, jwt
import logging

from src.schemas import User as UserSchema, UserCreate
from src.models import User, SessionLocal, init_db

# ログの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS 設定の追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# データベースの初期化
init_db()


# データベースセッションの取得
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# トークン検証関数
def verify_token(token: str):
    try:
        expected_audience = "<application id uri>"
        logger.info(f"Token: {token}")
        payload = jwt.decode(
            token,
            "",
            options={"verify_signature": False, "verify_exp": False},
            audience=expected_audience,
        )

        logger.info(f"Decoded token payload: {payload}")

        scp_claim = payload.get("scp")
        if scp_claim and "User.Read" in scp_claim:
            return True
        else:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")


@app.get("/users/", response_model=List[UserSchema])
def read_users(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    verify_token(token)
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@app.get("/users/{user_id}", response_model=UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    verify_token(token)
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/users/", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    verify_token(token)
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# デバッグ用エンドポイント
@app.get("/debug-token")
def debug_token(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(
        token,
        "",
        options={"verify_signature": False, "verify_exp": False},
        audience="<application id uri>",
    )
    return {"token_payload": payload}
