from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer


class Controller( Base ):
  """ Classe que representa cada endpoint no banco de dados do sistema """
  
  __tablename__ = "controller"

  id = Column(Integer, primary_key=True)
  nome = Column(String(255), unique=True, nullable=False)

  regras = relationship("regra", backref="controller", lazy=True)

  def __init__( self, nome: str ):
    self.nome = nome
  
  def __repr__( self ):
    return f"<Controller ${self.nome}>"