from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_database_url

DATABASE_URL = get_database_url()

engine = create_engine(
	DATABASE_URL,
	pool_pre_ping=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Session:
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()
