import json
from app.database import get_db
from app.models import userModel
from fastapi import APIRouter, Response, Depends
from sqlalchemy.orm import Session
from app.routers import paginate, instance_update
from app.swagger_models.userResponses import UserAllDoc, UserViewDoc
from app.swagger_models.generalResponses import DefaultReponseDoc
from app.schemas.userSchema import UserAddSchema, UserEditSchema

router = APIRouter(prefix="/user")


@router.get("/all", response_model=UserAllDoc)
async def userAll(db: Session = Depends(get_db)):
    users, output = paginate(db.query(userModel.User), 1, 10)

    for user in users:
        output["itens"].append(user.to_dict())

    return output

@router.get("/view/{id:int}", response_model=UserViewDoc)
async def userView(id: int, db: Session = Depends(get_db)):
    user = db.query(userModel.User).get(id)

    if not user:
        return {"error": True, "message": "user not found"}, 404
    
    response = {
        "error": False,
        "user": user.to_dict()
    }

    return response

@router.post("/add", response_model=DefaultReponseDoc)
async def userAdd(user: UserAddSchema, db: Session = Depends(get_db)):
    data = user.model_dump()
    email = data.get("email").lower()

    if db.query(userModel.User).filter(userModel.User.email == email).first():
        return Response(json.dumps({"error": True, "message": "email already registered"}), 409)
    
    newUser = userModel.User(
        data.get("name"),
        data.get("email").lower(),
        data.get("password"),
        False
    )
    db.add(newUser)

    try:
        db.flush()
        db.commit()
        return {"error": False, "message": "email criado com sucesso"}
    
    except:
        db.rollback()
        return {"error": True, "message": "database error"}

@router.put("/edit/{id:int}", response_model=DefaultReponseDoc)
async def userEdit(id: int, user: UserEditSchema, db: Session = Depends(get_db)):
    oldUser = db.query(userModel.User).get(id)

    if not oldUser:
        return {"error": True, "message": "user not found"}, 404

    data = user.model_dump()

    if "email" in data and data.get("email") is not None:
        repeatedEmail = db.query(userModel.User).filter(userModel.User.email == data.get("email")).first()

        if repeatedEmail:
            return {"error": True, "message": "Email already registered"}, 409

    instance_update(oldUser, data)
    db.add(oldUser)

    try:
        db.flush()
        db.commit()
        return {"error": False, "message": "deu bom"}
    
    except:
        db.rollback()
        return {"error": True, "message": "database error"}

@router.delete("/delete/{id:int}", response_model=DefaultReponseDoc)
async def userView(id: int, db: Session = Depends(get_db)):
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
