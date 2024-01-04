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

@router.put("/edit/{id:int}")
def userEdit(id: int, user: userSchema.UserEditSchema):
    db = get_db()

    oldUser = db.query(userModel.User).filter(userModel.User.id == id).first()

    if not oldUser:
        return {"error": True, "message": "user not found"}, 404

    if "email" in user.model_dump() and user.model_dump().get("email") is not None:
        repeatedEmail = db.query(userModel.User).filter(userModel.User.email == user.model_dump().get("email")).first()

        if repeatedEmail:
            return {"error": True, "message": "Email already registered"}, 409

    if "email" in user.model_dump() and user.model_dump().get("email") is not None:
        setattr(oldUser, "email", user.model_dump().get("email"))
    if "name" in user.model_dump() and user.model_dump().get("name") is not None:
        setattr(oldUser, "name", user.model_dump().get("name"))
    if "password" in user.model_dump() and user.model_dump().get("password") is not None:
        setattr(oldUser, "password", user.model_dump().get("password"))

    db.add(oldUser)

    try:
        db.flush()
        db.commit()
        return {"error": False, "message": "deu bom"}
    
    except:
        db.rollback()
        return {"error": True, "message": "database error"}

@router.delete("/delete/{id:int}")
def userView(id: int):
    db = get_db()

    user = db.query(userModel.User).filter(userModel.User.id == id).first()

    if not user:
        return {"error": True, "message": "user not found"}, 404
    
    db.delete(user)
    
    try:
        db.flush()
        db.commit()
        return {"error": False, "message": "deu bom"}

    except:
        db.rollback()
        return {"error": True, "message": "database error"}

