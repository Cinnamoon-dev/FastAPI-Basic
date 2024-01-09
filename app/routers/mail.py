# import os, jwt
# from app.database import get_db
# from pydantic import BaseModel, EmailStr
from fastapi import APIRouter, Response
# from starlette.responses import JSONResponse
# from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
# from typing import List

# from app.models.userModel import User

router = APIRouter(prefix="/mail")

# SECRET = 'd650537af22d543a085a9bac52ae25575c090e18'

# conf = ConnectionConfig(
#     MAIL_USERNAME= os.getenv('MAIL_USERNAME'),
#     MAIL_PASSWORD= os.getenv('MAIL_PASSWORD'),
#     MAIL_FROM= os.getenv('MAIL_FROM'),
#     MAIL_PORT= int(os.getenv('MAIL_PORT')),
#     MAIL_SERVER= "smtp.gmail.com",
#     MAIL_SSL_TLS=False,
#     USE_CREDENTIALS=True,
#     MAIL_STARTTLS=True,
#     VALIDATE_CERTS=True
# )

# class EmailSchema(BaseModel):
#     email: List[EmailStr]


# # async def send_email(email: EmailSchema, instance: User):
# #     token_data = {
# #         "id": instance.id,
# #         "username": instance.name
# #     }

# #     token = jwt.encode(token_data)
    
# @router.post("/email")
# async def simple_send(email: EmailSchema) -> JSONResponse:
#     html = """<p>Hi this test mail, thanks for using Fastapi-mail</p> """

#     message = MessageSchema(
#         subject="Fastapi-Mail module",
#         recipients=email.model_dump().get("email"),
#         body=html,
#         subtype=MessageType.html)

#     fm = FastMail(conf)
#     await fm.send_message(message)
#     return JSONResponse(status_code=200, content={"message": "email has been sent"})

from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import JSONResponse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


@router.post("/send-email/")
async def send_email(to_email: str, subject: str, body: str):
    # Your email credentials and SMTP server details
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'cinnamoonpeterdev@gmail.com'
    smtp_password = 'asdf1234**'

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        # Login to the email account
        server.login(smtp_username, smtp_password)

        # Send the email
        server.sendmail(smtp_username, to_email, msg.as_string())

        # Close the connection
        server.quit()

        return JSONResponse(content={"message": "Email sent successfully"}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))