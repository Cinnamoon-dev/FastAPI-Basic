from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer


class Cargo( Base ):
  """ Classe que representa cada cargo de um usuario no sistema  """
  
  __tablename__ = "cargo"

  id = Column(Integer, primary_key=True)
  nome = Column(String(255), nullable=False)

  users = relationship("Usuario", back_populates="cargo")

  def __init__( self, nome: str ):
    self.nome = nome

  def to_dict(self):
    data = {}
    data["id"] = self.id
    data["nome"] = self.nome

    return data

  def __repr__( self ):
    return f"<Controller ${self.id}, ${self.nome}"