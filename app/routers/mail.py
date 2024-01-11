import os
from dotenv import load_dotenv
from fastapi import APIRouter
from starlette.responses import JSONResponse
from app.schemas.mailSchema import EmailSchema
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

router = APIRouter(prefix="/mail")

load_dotenv()

MAIL_USERNAME = os.getenv("MAIL_USERNAME", "example@gmail.com")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "google_app_password")
MAIL_FROM = os.getenv("MAIL_FROM", MAIL_USERNAME)
NAME = os.getenv("NAME", "John Doe")
TITLE = "Example Title"

print(MAIL_USERNAME)
print(MAIL_PASSWORD)

conf = ConnectionConfig(
    MAIL_USERNAME = MAIL_USERNAME,
    MAIL_PASSWORD = MAIL_PASSWORD,
    MAIL_FROM = MAIL_FROM,
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME=NAME,
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

@router.post("/send")
async def simple_send(email: EmailSchema) -> JSONResponse:
    html = """<p>Hi this test mail, thanks for using Fastapi-mail</p>"""

    message = MessageSchema(
        subject=TITLE,
        recipients=email.model_dump().get("email"),
        body=html,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})