from jose import jwt
from starlette import status
from datetime import timedelta, datetime
from fastapi.responses import JSONResponse
from app.models.usuarioModel import Usuario
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter,  HTTPException, Depends
from . import db_dependency, form_auth_dependency, get_current_user, user_dependency
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


@router.post("/login", response_model = AuthResponseModel )
async def login( db : db_dependency, data_form : form_auth_dependency ):
    """ Endpoint de Login do sistema """

    user : Usuario = authenticate_user( (data_form.username).lower(), db)
   
    if not user:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=jsonable_encoder({"error" : True, "message" : "Usuário não encontrado"}))

    if user.is_verified == False:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=jsonable_encoder({"error" : False, "message" : "Usuário com email não verificado"}))

    if not bcrypt_context.verify(data_form.password, user.password):
        return JSONResponse(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            content=jsonable_encoder({"error" : True, "message" : "Credenciais incorretas"}))

    token = create_access_token( user.email, user.id, timedelta( 
        minutes = ACCESS_TOKEN_EXPIRE_MINUTES
    ) )
    refresh_token = create_refresh_token( user.email, user.id, timedelta(
        days = REFRESH_TOKEN_EXPIRE_DAYS
    ) )
    
    content_response = jsonable_encoder({
        "token_type": "Bearer",
        "access_token" : token,
        "refresh_token" : refresh_token,
    })
    
    return JSONResponse( status_code=status.HTTP_202_ACCEPTED, content=jsonable_encoder(content_response) )


@router.get("/me", status_code = status.HTTP_200_OK, response_model=MeResponseModel)
async def get_user_credentials( user : user_dependency ):
    """ Endpoint para retornar os dados do user logado """

    if user is None:
        raise HTTPException(
            detail="Authentication fail", 
            status_code=status.HTTP_400_BAD_REQUEST
        )

    return JSONResponse( content=user, status_code=status.HTTP_200_OK )


@router.get("/refresh", response_model=RefreshTokenResponse, dependencies=[Depends(get_current_user)])
async def refresh_token():
    """ Endpoint para renovação de token """
    
    user = get_current_user()

    new_access_token = create_refresh_token(
        email=user["email"],
        user_id=user["user_id"],
        expires_delta= timedelta( 
        minutes = ACCESS_TOKEN_EXPIRE_MINUTES
    ))
    
    reponse_data = {"access_token" : new_access_token}

    return JSONResponse( content=reponse_data, status_code=status.HTTP_200_OK )


def authenticate_user(email : str, db : db_dependency):
    """ 
        Function to validate if a user exist in db 

        returns usuario_instance if exist user in database
        returns false if user_email dont match with a user in db
    """

    user : Usuario = db.query(Usuario).filter( Usuario.email == email ).first()
    return user if user is not None else False


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