"""
    Duplicando pois é necessário outro arquivo para importar as definições de dentro do package database.
    O arquivo insertData.py não 'enxerga' o __init__.py, e os arquivos externos não conseguem 'enxergar' o imports.py,
    logo os dois se fazem necessários.
"""


import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

STAGE = os.getenv("STAGE", None)
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL", "postgresql://postgres:1234@localhost:5432/fastdb")

if STAGE == "test":
    SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_TEST_URL", "postgresql://postgres:1234@localhost:5432/postgres")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    def _get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    return next(_get_db())