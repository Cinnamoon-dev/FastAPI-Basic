from pydantic import BaseModel

class UserSchema(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        orm_mode = True