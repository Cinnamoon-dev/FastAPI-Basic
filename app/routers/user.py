from app.database import get_db
from app.models import userModel
from app.schemas import userSchema
from fastapi import APIRouter, Request
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

@router.get("/view/{id:int}")
def userView(id: int):
    db = get_db()

    user = db.query(userModel.User).filter(userModel.User.id == id).first()

    if not user:
        return {"error": True, "message": "user not found"}, 404
    
    response = {
        "error": False,
        "user": user.to_dict()
    }

    return response
    
@router.post("/add")
def userAdd(user: userSchema.UserSchema):
    db = get_db()
    newUser = userModel.User(user.name, user.email, user.password)

    db.add(newUser)

    try:
        db.flush()
        db.commit()
        return {"error": False, "message": "deu bom"}
    
    except:
        db.rollback()
        return {"error": True, "message": "database error"}