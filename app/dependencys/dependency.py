from typing import Annotated
from starlette import status
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from app import ALGORITHM, JWT_ACCESS_SECRETY_KEY
from fastapi.security import OAuth2PasswordBearer


# função para obter o usuario logado, funciona como o decorator.
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user( token : Annotated[str, Depends(oauth2_bearer)] ):
  try:
    payload = jwt.decode(token, JWT_ACCESS_SECRETY_KEY, algorithms=[ALGORITHM])
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