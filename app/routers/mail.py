from fastapi import APIRouter, Response
from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List

router = APIRouter(prefix="/mail")

conf = ConnectionConfig(
    MAIL_USERNAME = "cinnamoonpeterdev@gmail.com",
    MAIL_PASSWORD = "asdf1234**",
    MAIL_FROM = "cinnamoonpeterdev@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="FastAPI-Mail Test",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = False,
    VALIDATE_CERTS = False
)

class EmailSchema(BaseModel):
    email: List[EmailStr]

@router.post("/email")
async def simple_send(email: EmailSchema) -> JSONResponse:
    html = """<p>Hi this test mail, thanks for using Fastapi-mail</p> """

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.dict().get("email"),
        body=html,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})