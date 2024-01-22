from app.database import Base
from app.models import controllerModel, cargoModel
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean


class Regra( Base ):
  """ Classe que representa cada endpoint no banco de dados do sistema """
  
  __tablename__ = "regra"

  id = Column(Integer, primary_key=True)
  action = Column(String(255), nullable=False)
  cargo_id = Column( 
    Integer, ForeignKey(cargoModel.Cargo.id), nullable=False, primary_key=True
  )
  controller_id = Column(
    Integer, ForeignKey(controllerModel.Controller.id), nullable=False, primary_key=True
  )
  
  permitir = Column(Boolean, nullable=False)

  def __init__( self, acao : str, cargo_id : int, permitir: bool, controller_id : int ):
    self.action = acao
    self.cargo_id = cargo_id
    self.permitir = permitir
    self.controller_id = controller_id

  def to_dict(self):
    data = {}
    data["action"] = self.action
    data["permitir"] = self.permitir
    data["controller_id"] = self.controller_id

    return data

  def __repr__( self ):
    return (
      f"<Regra {self.id}, {self.action}, {self.cargo_id}, {self.controller_id}, {self.permitir}>"
    )