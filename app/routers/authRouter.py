import json
from fastapi import APIRouter, Response
from pydantic import BaseModel

from app.database import get_db
from app.models import userModel

router = APIRouter(prefix="/auth")

class Auth(BaseModel):
    email : str
    password : str


@router.post("/")
async def auth( request : Auth ):
    db = get_db()

    users = db.query(userModel.User).filter( userModel.User.email == request.email ).first()

    if users is None:
        object_response = json.dumps({"message": "Usuário não encontrado", "error" : True})
        return Response( status_code=404, content=object_response )



    return request