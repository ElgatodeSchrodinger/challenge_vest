from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi_utils.session import FastAPISessionMaker

from core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
sessionmakerFastAPI = FastAPISessionMaker(settings.SQLALCHEMY_DATABASE_URI)


def get_db():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    finally:
        session.close()
