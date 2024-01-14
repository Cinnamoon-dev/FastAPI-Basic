from pydantic import BaseModel

class AuthRequestModel(BaseModel):
  email : str
  password : str

class AuthResponseModel(BaseModel):
  access_token : str
  refresh_token : str
