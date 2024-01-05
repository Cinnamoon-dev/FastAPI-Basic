from fastapi import APIRouter, Request
from app.database import get_db
from app.models import userModel
from app.routers import paginate
from app.schemas import userSchema

router = APIRouter(prefix="/user")


@router.get("/all")
async def userAll():
    db = get_db()
    users, output = paginate(db.query(userModel.User), 1, 10)

    for user in users:
        output["itens"].append(user.to_dict())

    return output

@router.get("/view/{id:int}")
async def userView(id: int):
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
async def userAdd(request: Request):
    db = get_db()
    data = await request.json()

    email = data.get("email").lower()

    if db.query(userModel.User).filter(userModel.User.email == email).first():
        return {"error": True, "message": "email already registered"}, 409
    
    newUser = userModel.User(
        data.get("name"),
        data.get("email").lower(),
        data.get("password")
    )
    db.add(newUser)

    try:
        db.flush()
        db.commit()
        return {"error": False, "message": "email criado com sucesso"}
    
    except:
        db.rollback()
        return {"error": True, "message": "database error"}

@router.put("/edit/{id:int}")
async def userEdit(id: int, request: Request):
    db = get_db()
    oldUser = db.query(userModel.User).get(id)

    if not oldUser:
        return {"error": True, "message": "user not found"}, 404

    data = await request.json()

    if "email" in data and data.get("email") is not None:
        repeatedEmail = db.query(userModel.User).filter(userModel.User.email == data.get("email")).first()

        if repeatedEmail:
            return {"error": True, "message": "Email already registered"}, 409

    if "email" in data and data.get("email") is not None:
        setattr(oldUser, "email", data.get("email"))

    if "name" in data and data.get("name") is not None:
        setattr(oldUser, "name", data.get("name"))

    if "password" in data and data.get("password") is not None:
        setattr(oldUser, "password", data.get("password"))

    db.add(oldUser)

    try:
        db.flush()
        db.commit()
        return {"error": False, "message": "deu bom"}
    
    except:
        db.rollback()
        return {"error": True, "message": "database error"}

@router.delete("/delete/{id:int}")
async def userView(id: int):
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
