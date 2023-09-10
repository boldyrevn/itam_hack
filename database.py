from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings

engine = create_engine(settings.postgres_url, echo=True)

SessionLocal = sessionmaker(engine, autobegin=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
