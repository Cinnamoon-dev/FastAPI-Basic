import os, json
from fastapi import APIRouter, Response
from dotenv import load_dotenv
from app.database import get_db
from app.models.userModel import User
from starlette.responses import JSONResponse
from app.schemas.mailSchema import SendEmailSchema, VerifyEmailSchema
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

router = APIRouter(prefix="/mail")

load_dotenv()

MAIL_USERNAME = os.getenv("MAIL_USERNAME", "example@gmail.com")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "google_app_password")
MAIL_FROM = os.getenv("MAIL_FROM", MAIL_USERNAME)
NAME = os.getenv("NAME", "John Doe")
TITLE = "Example Title"

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

@router.post("/send_verify_email")
async def send_verify_email(email: SendEmailSchema) -> JSONResponse:
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

@router.post("/verify_email")
async def verify_email(email: VerifyEmailSchema):
    db = get_db()
    user = db.query(User).filter(User.email == email.model_dump()["email"]).first()

    if not user:
        return Response(json.dumps({"error": True, "message": "Email not found"}), 404)
    
    user.isVerified = True

    try:
        db.commit()
        return Response(json.dumps({"error": False, "message": "User verified successfully"}))
    
    except:
        db.rollback()
        return Response(json.dumps({"error": True, "message": "database error"}))