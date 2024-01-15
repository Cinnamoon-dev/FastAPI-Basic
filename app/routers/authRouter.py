from jose import jwt
from starlette import status
from app.models.userModel import User
from datetime import timedelta, datetime
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter,  HTTPException
from app.dependencys.dependency import token_dependency
from app.dependencys import db_dependency, user_dependency, form_auth_dependency
from app.schemas.AuthSchema import AuthResponseModel, MeResponseModel, RefreshTokenResponse
from app import ( 
    bcrypt_context, 
    ALGORITHM_TO_HASH, 
    JWT_ACCESS_SECRETY_KEY, 
    JWT_REFRESH_SECRET_KEY, 
    REFRESH_TOKEN_EXPIRE_DAYS,
    ACCESS_TOKEN_EXPIRE_MINUTES, 
)


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=AuthResponseModel)
async def login( db : db_dependency, data_form : form_auth_dependency ):
    """ Endpoint de Login do sistema """

    user = authenticate_user(data_form.username, data_form.password, db)
   
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Usuário não encontrado", "error": True}
        )

    token = create_access_token( user.email, user.id, timedelta( 
        minutes = ACCESS_TOKEN_EXPIRE_MINUTES
    ) )
    refresh_token = create_refresh_token( user.email, user.id, timedelta(
        days = REFRESH_TOKEN_EXPIRE_DAYS
    ) )
    
    content_response = jsonable_encoder({
        "token_type": "bearer",
        "access_token" : token,
        "refresh_token" : refresh_token,
    })
    
    response = JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content=jsonable_encoder(content_response), 
    )

    return response


@router.get("/me", status_code = status.HTTP_200_OK, response_model=MeResponseModel)
async def get_user_credentials( user : user_dependency ):
    """ Endpoint para retornar os dados do user logado """
    
    if user is None:
        raise HTTPException(
            detail="Authentication fail", 
            status_code=status.HTTP_400_BAD_REQUEST
        )

    return JSONResponse( content=user, status_code=status.HTTP_200_OK )


@router.get("/refresh", response_model=RefreshTokenResponse)
async def refresh_token( user : user_dependency ):
    """ Endpoint para renovação de token """
    
    new_access_token = create_refresh_token(
        email=user["email"],
        user_id=user["user_id"],
        expires_delta= timedelta( 
        minutes = ACCESS_TOKEN_EXPIRE_MINUTES
    ))
    
    reponse_data = {"access_token" : new_access_token}

    return JSONResponse( content=reponse_data, status_code=status.HTTP_200_OK )


def authenticate_user(email : str, password: str, db) -> bool | User:
    user : User = db.query(User).filter( User.email == email ).first()

    if user is None or not bcrypt_context.verify(password, user.password):
        return False
    
    return user


def create_access_token( email: str, user_id : int, expires_time: timedelta ) -> str:
    encode = {'email' : email, 'user_id' : user_id}
    expires = datetime.utcnow() + expires_time
    encode.update({'exp' : expires})
    
    return jwt.encode(encode, JWT_ACCESS_SECRETY_KEY, algorithm=ALGORITHM_TO_HASH)


def create_refresh_token( email : str, user_id : int, expires_delta: timedelta) -> str:
    encode = {'email' : email, 'user_id' : user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp" : expires})

    return jwt.encode(encode, JWT_REFRESH_SECRET_KEY, ALGORITHM_TO_HASH)