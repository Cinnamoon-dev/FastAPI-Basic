import json
from app import bcrypt_context
from app.database import get_db
from sqlalchemy.orm import Session
from app.models.usuarioModel import Usuario
from fastapi import APIRouter, Response, Depends
from . import PermissionChecker, get_current_user
from app.routers import paginate, instance_update
from app.schemas.userSchema import UserAddSchema, UserEditSchema
from app.swagger_models.generalResponses import DefaultReponseDoc
from app.swagger_models.userResponses import UserAllDoc, UserViewDoc



router = APIRouter(prefix="/user", tags=["user"])


@router.get("/all/notVerified")
async def userAllNotVerified(
        db = Depends(get_db),
        authorize: bool = Depends(PermissionChecker(required_permission="usuario-all"))
    ):
    """
        Endpoint para retornar todos os usuarios que não foram verificados no 
        sistema.
    """

    all_user_not_verified_query = Usuario.is_verified == False
    query = get_query_user_by_restriction( restriction= all_user_not_verified_query, db= db )
    users, output = paginate(query, 1, 10)

    for user in users:
        output["itens"].append(user.to_dict())

    return output


@router.get("/all", response_model=UserAllDoc)
async def userAll( 
        db = Depends(get_db),
        authorize: bool = Depends(PermissionChecker(required_permission="usuario-all"))
    ):
    """
        Endpoint que retorna todos os usuarios independente se ele esta
        verificado ou não.
    """

    all_user_query = Usuario.is_verified == True
    query = get_query_user_by_restriction( restriction= all_user_query, db= db )
    users, output = paginate(query, 1, 10)

    for user in users:
        output["itens"].append(user.to_dict())

    return output


@router.get("/view/{id:int}", response_model=UserViewDoc, dependencies=[Depends(get_current_user)])
async def userView(
        id: int, 
        db: Session = Depends(get_db),
        authorize: bool = Depends(PermissionChecker(required_permission="usuario-view"))
    ):
    user = db.query(Usuario).get(id)

    if not user:
        return {"error": True, "message": "user not found"}, 404
    
    response = {
        "error": False,
        "user": user.to_dict()
    }

    return response


@router.post("/add", response_model=DefaultReponseDoc)
async def userAdd( user: UserAddSchema, db: Session = Depends(get_db) ):
    data = user.model_dump()
    email = data.get("email").lower()

    if db.query(Usuario).filter(Usuario.email == email).first():
        return Response(json.dumps({"error": True, "message": "email already registered"}), 409)
    
    newUser = Usuario(
        is_verified =False,
        name        =data.get("name"),
        cargo_id    =data.get("cargo_id"),
        email       =data.get("email").lower(),
        password    =bcrypt_context.hash(data.get("password"))
    )
    db.add(newUser)

    try:
        db.flush()
        db.commit()
        return {"error": False, "message": "email criado com sucesso"}
    
    except:
        db.rollback()
        return {"error": True, "message": "database error"}


@router.put("/edit/{id:int}", response_model=DefaultReponseDoc, dependencies=[Depends(get_current_user)])
async def userEdit(
        id: int, user: UserEditSchema, 
        db: Session = Depends(get_db),
        authorize: bool = Depends(PermissionChecker(required_permission="usuario-all"))
    ):
    oldUser = db.query(Usuario).get(id)

    if not oldUser:
        return {"error": True, "message": "user not found"}, 404

    data = user.model_dump()

    if data.get("email") is not None:
        lower_email = data.get("email").lower()
        repeatedEmail = db.query(Usuario).filter(Usuario.email == lower_email).first()

        if repeatedEmail:
            return {"error": True, "message": "Email already registered"}, 409

    instance_update(oldUser, data)
    
    try:
        db.commit()
        return {"error": False, "message": "deu bom"}
    
    except:
        db.rollback()
        return {"error": True, "message": "database error"}


@router.delete("/delete/{id:int}", response_model=DefaultReponseDoc, dependencies=[Depends(get_current_user)])
async def userView( 
        id: int, 
        db: Session = Depends(get_db),
        authorize: bool = Depends(PermissionChecker(required_permission="usuario-delete"))
    ):
    user = db.query(Usuario).filter(Usuario.id == id).first()

    if not user:
        return {"error": True, "message": "user not found"}, 404
    
    db.delete(user)
    
    try:
        db.commit()
        return {"error": False, "message": "deu bom"}

    except:
        db.rollback()
        return {"error": True, "message": "database error"}


def get_query_user_by_restriction( restriction : any, db : Session ):
    """
        Função que retorna os usuarios com base em uma restrição
        essa restrição deve ser válida para a tabela Usuario.

        Retorna uma query que pode ser inserida diretamente no paginate.
    """
    return db.query( Usuario ).filter( restriction )