"""
    Duplicando pois é necessário outro arquivo para importar as definições de dentro do package database.
    O arquivo insertData.py não 'enxerga' o __init__.py, e os arquivos externos não conseguem 'enxergar' o imports.py,
    logo os dois se fazem necessários.
"""


import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

USER = os.getenv("POSTGRES_USER", "postgres")
PASSWORD = os.getenv("POSTGRES_PASSWORD", "1234")
HOST = os.getenv("POSTGRES_HOST", "localhost")
PORT = os.getenv("POSTGRES_PORT", 5432)
DATABASE = os.getenv("POSTGRES_DB", "fastdb")
TEST_DATABASE = os.getenv("TEST_POSTGRES_DB", "postgres")

SQLALCHEMY_DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
SQLALCHEMY_DATABASE_TEST_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{TEST_DATABASE}"

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