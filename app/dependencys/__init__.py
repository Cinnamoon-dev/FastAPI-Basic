from typing import Annotated
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from .dependency import get_current_user
from fastapi.security import  OAuth2PasswordRequestForm

# dependencys

db_dependency = Annotated[Session, Depends(get_db)]
form_auth_dependency = Annotated[OAuth2PasswordRequestForm, Depends()]

user_dependency = Annotated[dict, Depends(get_current_user)]