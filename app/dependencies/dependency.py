from typing import Annotated
from starlette import status
from jose import JWTError, jwt
from app.models.userModel import User
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app import ALGORITHM_TO_HASH, JWT_ACCESS_SECRETY_KEY
from app.dependencies import user_dependency, db_dependency


# função para obter o usuario logado, funciona como o decorator.
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")
token_dependency = Annotated[str, Depends(oauth2_bearer)]

def get_current_user( token : token_dependency ):
  try:
    payload = jwt.decode(token, JWT_ACCESS_SECRETY_KEY, algorithms=[ALGORITHM_TO_HASH])
    email : str = payload.get("email")
    user_id : int = payload.get("user_id")

    if None in [email, user_id]:
      raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail={"message": "Não foi possível encontrar o user", "error": True}
      )
    return {"email" : email, "user_id" : user_id}
  
  except JWTError:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"message": "Não foi possível encontrar o user", "error": True}
    )
  
def resource( 
    resouce_name : str, 
    db : db_dependency,
    user : user_dependency, 
  ):
  
  user_instance : User = db.session.query(User).get(user["user_id"])
  user_role = user_instance.cargo

  
  return