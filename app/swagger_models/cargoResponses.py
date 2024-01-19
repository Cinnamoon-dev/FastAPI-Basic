from pydantic import BaseModel

class CargoDoc(BaseModel):
  id : int
  nome : str