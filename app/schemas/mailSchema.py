from typing import List
from pydantic import BaseModel, EmailStr

class SendEmailSchema(BaseModel):
    email: List[EmailStr]

class VerifyEmailSchema(BaseModel):
    email: EmailStr