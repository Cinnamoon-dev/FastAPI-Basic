from pydantic import BaseModel
from app.swagger_models.cargoResponses import CargoDoc
from app.swagger_models.generalResponses import PaginationDoc

class UserDoc(BaseModel):
    id: int
    name: str
    email: str
    password: str
    isVerified: bool
    cargo : CargoDoc

class UserAllDoc(BaseModel):
    error: bool = False
    itens: list[UserDoc]
    pagination: PaginationDoc

class UserViewDoc(BaseModel):
    user: UserDoc
    error: bool