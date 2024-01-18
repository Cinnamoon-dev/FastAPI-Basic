from pydantic import BaseModel
from typing import Optional

class UserAddSchema(BaseModel):
    name: str
    email: str
    password: str
    cargo_id : int

    model_config = {
        "cargo_id" : 1,
        "name": "user",
        "email": "user@email.com",
        "password": "password"
    }

class UserEditSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str]  = None
    cargo_id : Optional[int] = None

    model_config = {
        "cargo_id" : 1,
        "name": "user",
        "email": "user@email.com",
        "password": "password"
    }
