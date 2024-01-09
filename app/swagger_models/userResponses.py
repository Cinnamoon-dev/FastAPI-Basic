from pydantic import BaseModel
from app.swagger_models.generalResponses import PaginationDoc

class UserDoc(BaseModel):
    id: int
    name: str
    email: str
    password: str

class UserAllDoc(BaseModel):
    error: bool
    itens: list[UserDoc]
    pagination: PaginationDoc

class UserViewDoc(BaseModel):
    user: UserDoc
    error: bool