from pydantic import BaseModel


class AuthResponseModel(BaseModel):
  token_type : str
  access_token : str
  refresh_token : str

class MeResponseModel(BaseModel):
  id : str
  email : str

class RefreshTokenResponse:
  access_token : str
  access_token = "HASH DO TOKEN"