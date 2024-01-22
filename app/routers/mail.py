import os, json
from typing import Union
from pydantic import EmailStr
from dotenv import load_dotenv
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from app.models.usuarioModel import Usuario
from starlette.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from app.schemas.mailSchema import SendEmailSchema
from fastapi import APIRouter, Request, Response, Depends
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from itsdangerous import URLSafeTimedSerializer, BadTimeSignature, SignatureExpired

from app.swagger_models.mailResponses import ForgotPasswordDoc

router = APIRouter(prefix="/mail", tags=["mail"])
templates = Jinja2Templates(directory="templates")

load_dotenv()

MAIL_USERNAME = os.getenv("MAIL_USERNAME", "example@gmail.com")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "google_app_password")
MAIL_FROM = os.getenv("MAIL_FROM", MAIL_USERNAME)
NAME = os.getenv("NAME", "John Doe")
TITLE = "Example Title"
EMAIL_SECRET_KEY = os.getenv("EMAIL_SECRET_KEY", "[->SecretKeyHere!!!<-]")

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

token_algo = URLSafeTimedSerializer(EMAIL_SECRET_KEY, salt="Email_verification_&_Forgot_password")

def token(email: EmailStr):
    _token = token_algo.dumps(email)
    return _token

async def send_email(html, title, email):
    message = MessageSchema(
        subject=title,
        recipients=[email],
        body=html.body,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)

@router.post("/send_verify_email")
async def send_verify_email(email: SendEmailSchema, request: Request, db: Session = Depends(get_db)):
    
    email_to_verify = str(email.model_dump()["email"]).lower()
    user = db.query(Usuario).filter(Usuario.email == email_to_verify).first()

    if not user:
        return Response(json.dumps({"error": True, "message": "Email not found"}), 404)

    email_token = token(email_to_verify)
    html = templates.TemplateResponse(request=request, name="emailVerify.html", context={"email_token": email_token})

    await send_email(html, TITLE, email_to_verify)    
    return JSONResponse(status_code=200, content={"message": "email has been sent", "error": False})


@router.get("/verify_email/{email_token}", response_class=HTMLResponse)
async def verify_email(request: Request, email_token: Union[str, bytes], db: Session = Depends(get_db)):

    try:
        email = token_algo.loads(email_token, max_age=1800).lower()

    except SignatureExpired:
        return templates.TemplateResponse(request=request, name="emailExpired.html")
    
    except BadTimeSignature:
        return templates.TemplateResponse(request=request, name="emailInvalidToken.html")

    user = db.query(Usuario).filter(Usuario.email == email).first()
    user.is_verified = True

    try:
        db.commit()
        return templates.TemplateResponse(request=request, name="emailSuccess.html")
    
    except:
        db.rollback()
        return templates.TemplateResponse(request=request, name="databaseError.html")


@router.post("/forgot_password", response_model=ForgotPasswordDoc)
async def forgotPassword(request: Request, db: Session = Depends(get_db)):

    data = await request.json()
    user = db.query(Usuario).filter(Usuario.email == data["email"].lower()).first()

    if not user:
        return Response(json.dumps({"message": "User not found", "error": True}), status_code=404)
    
    user.password = data["newPassword"]

    try:
        db.commit()
        return Response(content=json.dumps({"message": "Password updated", "error": False}), status_code=200)
    
    except:
        db.rollback()
        return Response(content=json.dumps({"message": "Database Error", "error": True}), status_code=500)