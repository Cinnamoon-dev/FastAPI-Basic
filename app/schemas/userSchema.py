from pydantic import BaseModel
from typing import Optional

class UserAddSchema(BaseModel):
    name: str
    email: str
    password: str

    model_config = {
        "name": "user",
        "email": "user@email.com",
        "password": "password"
    }

    class Config:
        orm_mode = True

class UserEditSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str]  = None

    model_config = {
        "name": "user",
        "email": "user@email.com",
        "password": "password"
    }

    class Config:
        orm_mode = True
