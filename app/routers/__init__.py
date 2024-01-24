import math
from typing import Annotated
from starlette import status
from jose import JWTError, jwt
from sqlalchemy.orm import Query
from sqlalchemy.orm import Session
from app.models.regraModel import Regra
from app.database.imports import get_db
from fastapi import Depends, HTTPException
from app.models.usuarioModel import Usuario
from app.models.controllerModel import Controller
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from app import ALGORITHM_TO_HASH, JWT_ACCESS_SECRETY_KEY, bcrypt_context

# exportando types annotations que vão ser muito utilizadas
db_dependency = Annotated[Session, Depends(get_db)]
form_auth_dependency = Annotated[OAuth2PasswordRequestForm, Depends()]

# -------------------------------------------------------------------------------------------------- #

# item pagination
def paginate(query: Query, page: int = 1, rows_per_page: int = 1):
    itens_count = query.count()
    pages_count = math.ceil(itens_count / rows_per_page)
    prev = None
    next = None

    if page - 1 > 0:
        prev = page - 1
    
    if page + 1 < pages_count :
        next = page + 1

    output = {
        "itens": [],
        "pagination": {
            "pages_count": pages_count,
            "itens_count": itens_count,
            "itens_per_page": rows_per_page,
            "prev": prev,
            "next": next,
            "current": page
        },
        "error": False
    }

    start = page * rows_per_page - rows_per_page
    stop = page * rows_per_page

    itens = query.slice(start, stop)
    return itens, output

# -------------------------------------------------------------------------------------------------- #

# update table line
def instance_update(instance, request_json):
    """
    This function updates every key received from the request in an instance of a table, if the key exists in that table.
    
    Example: The table User has three columns (id, name, email) and the request object has five fields (name, age, bloodType, email, address).
    The updated fields in the instance will be (name, email).

    The parameter instance should be a query from a table. 

    `instance = User.query.get(id)`
    """

    instance_keys : list[str] = list(instance.to_dict().keys())

    for key in instance_keys:
      if key in request_json and request_json[key] is not None:
        setattr(instance, key, request_json.get(key))
    
    if request_json.get("email") is not None:
      setattr(instance, 'email', request_json.get("email").lower())
    
    if request_json.get("password") is not None:
      setattr(instance, 'password', bcrypt_context.hash(request_json.get("password")))

# -------------------------------------------------------------------------------------------------- #
# JWT Validator

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")
token_dependency = Annotated[str, Depends(oauth2_bearer)]

def get_current_user( token : token_dependency ):
  """ Dependencia para obter o usuario logado.  """
  
  try:
    payload = jwt.decode(token, JWT_ACCESS_SECRETY_KEY, algorithms=[ALGORITHM_TO_HASH])
    email : str = payload.get("email")
    user_id : int = payload.get("user_id")

    if None in [email, user_id]:
      raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail={"message": "Usuario não autorizado", "error" : True}
      )
    return {"email" : email, "user_id" : user_id}
  
  except JWTError:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"message": "Usuario não autorizado", "error" : True}
  )

user_dependency = Annotated[dict, Depends(get_current_user)]

# -------------------------------------------------------------------------------------------------- #
# access control

class PermissionChecker:

  def __init__(self, required_permission: str) -> None:
    self.required_permission = required_permission

  def __call__(
    self,
    db : Session = Depends(get_db),  
    user: dict = Depends(get_current_user),
  ) -> bool:

    controller, action = self.required_permission.split("-")
    user_instance : Usuario = db.query(Usuario).get(user["user_id"])
    user_role = user_instance.cargo_id

    data = db.query(
      Regra.permitir,
      Regra.cargo_id,
      Regra.action.label("action"),
      Controller.nome.label("controller")

    ).join( Controller, Regra.controller_id == Controller.id ).filter(
      Regra.action == action,
      Regra.cargo_id == user_role,
      Controller.nome == controller

    ).first()

    if data is None or not data.permitir:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"description" : "Usuario não autorizado"},
      )    

    return True
