from app.database import get_db
from app.models import userModel
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/user")


@router.get("/all")
def userAll():
    db = get_db()

    users = db.query(userModel.User).all()
    
    data = {
        "error": False,
        "items": users
    }

    return data
