from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
metadata = MetaData()

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)
    # 初期データの挿入
    db = SessionLocal()
    if db.query(User).count() == 0:
        db.add_all(
            [
                User(name="Alice", email="alice@example.com"),
                User(name="Bob", email="bob@example.com"),
                User(name="Charlie", email="charlie@example.com"),
            ]
        )
        db.commit()
    db.close()
