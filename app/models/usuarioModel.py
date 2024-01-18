from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import BigInteger, Column, String, Boolean, Integer, ForeignKey

class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_verified = Column(Boolean, nullable=False)
    email = Column(String, unique=True, nullable=False)

    cargo_id = Column(BigInteger, ForeignKey("cargo.id"), nullable=False)
    cargo = relationship("Cargo", back_populates="users",foreign_keys=[cargo_id])

    def __init__(self, name, email, password, is_verified, cargo_id):
        self.name = name
        self.email = email
        self.password = password
        self.cargo_id = cargo_id
        self.is_verified = is_verified

    def to_dict(self):
        data = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "cargo" : self.cargo.to_dict(),
            "isVerified": self.is_verified,
        }

        return data

    def __repr__(self):
        return f"<User {self.id} {self.name} {self.email} {self.password} {self.is_verified}>" 