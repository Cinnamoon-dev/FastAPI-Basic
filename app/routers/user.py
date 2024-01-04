from fastapi import APIRouter, Request
from app.database import get_db
from app.models import userModel
from app.schemas import userSchema

router = APIRouter(prefix="/user")


@router.get("/all")
def userAll():
    # TODO
    # Paginate with db.query.slice and db.query.count
    db = get_db()
    users = db.query(userModel.User).all()
    
    data = {
        "error": False,
        "items": []
    }

    for user in users:
        user_json = user.to_dict()
        data["items"].append(user_json)

    return data

@router.get("/view/{id:int}")
def userView(id: int):
    db = get_db()
    user = db.query(userModel.User).get(id)

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
    
    if db.query(userModel.User).filter(userModel.User.email == user.email.lower()).first():
        return {"error": True, "message": "email already registered"}, 409
    
    newUser = userModel.User(user.name, user.email.lower(), user.password)
    db.add(newUser)

    try:
        db.flush()
        db.commit()
        return {"error": False, "message": "email criado com sucesso"}
    
    except:
        db.rollback()
        return {"error": True, "message": "database error"}

@router.put("/edit/{id:int}")
def userEdit(id: int, user: userSchema.UserEditSchema):
    db = get_db()
    oldUser = db.query(userModel.User).get(id)

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

