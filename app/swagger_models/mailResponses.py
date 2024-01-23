from pydantic import BaseModel, EmailStr

class ForgotPasswordDoc(BaseModel):
    email: EmailStr
    newPassword: str

class SendVerifyEmailDocSuccess(BaseModel):
    message: str
    error: bool = False