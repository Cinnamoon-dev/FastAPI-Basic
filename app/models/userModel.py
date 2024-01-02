from app.database import Base
from sqlalchemy import BigInteger, Column, String


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)