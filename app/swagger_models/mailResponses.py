from pydantic import BaseModel, EmailStr

class ForgotPasswordDoc(BaseModel):
    email: EmailStr
    newPassword: str