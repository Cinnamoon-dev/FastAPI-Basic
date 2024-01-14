import os, json
from typing import Union
from fastapi import APIRouter, Request, Response, Depends
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from pydantic import EmailStr
from app.database import get_db
from itsdangerous import URLSafeTimedSerializer, BadTimeSignature, SignatureExpired
from app.models.userModel import User
from starlette.responses import JSONResponse
from app.schemas.mailSchema import SendEmailSchema
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

token_algo = URLSafeTimedSerializer("asdfqwerty", salt="Email_verification_&_Forgot_password")

def token(email: EmailStr):
    _token = token_algo.dumps(email)
    return _token

@router.post("/send_verify_email")
async def send_verify_email(email: SendEmailSchema, request: Request, db: Session = Depends(get_db)):
    email_to_verify = str(email.model_dump()["email"])
    user = db.query(User).filter(User.email == email_to_verify).first()

    if not user:
        return Response(json.dumps({"error": True, "message": "Email not found"}), 404)

    email_token = token(email_to_verify)

    html = f"""
    <p>
        Click in the following link to confirm your email: 
        <a href="{request.url_for("verify_email",email_token= email_token)}">link</a>
    </p>
    """

    message = MessageSchema(
        subject=TITLE,
        recipients=[email.model_dump().get("email")],
        body=html,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})

@router.get("/verify_email/{email_token}", response_class=HTMLResponse)
async def verify_email(email_token: Union[str, bytes], db: Session = Depends(get_db)):

    try:
        email = token_algo.loads(email_token, max_age=1800)
    except SignatureExpired:
        return "<p>Tempo expirado, peça outro email.</p>"
    except BadTimeSignature:
        return "<p>Token invalido, peça outro email.</p>"

    user = db.query(User).filter(User.email == email).first()
    user.isVerified = True

    try:
        db.commit()
        return "<p>User verified successfully</p>"
    
    except:
        db.rollback()
        return "<p>Database Error, try again later.</p>"