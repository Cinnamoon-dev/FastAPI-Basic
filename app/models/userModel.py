from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import BigInteger, Column, String, Boolean, Integer, ForeignKey


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True)
    password = Column(String, nullable=False)
    isVerified = Column(Boolean, nullable=False)

    cargo_id = Column(Integer,ForeignKey("cargo.id"), nullable=False)

    def __init__(self, name, email, password, isVerified):
        self.name = name
        self.email = email
        self.password = password
        self.isVerified = isVerified

    def to_dict(self):
        data = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "isVerified": self.isVerified
        }

        return data

    def __repr__(self):
        return f"<User {self.id} {self.name} {self.email} {self.password} {self.isVerified}>" 