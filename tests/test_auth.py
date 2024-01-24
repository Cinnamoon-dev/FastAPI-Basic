
""" 
  Arquivo de teste de autenticação.

  PS: Para simular um formdata é necessário passar data no client.post.
      ele simula um formdata que viria do frontend.
"""

def test_login_with_not_found_user(client_app):

  valid_user = {"username" : "notFound@email.com", "password": "1234"}
  response = client_app.post("/auth/login",data=valid_user)

  assert not response.is_success
  assert response.status_code == 404
  assert "access_token" not in response.json()
  assert "refresh_token" not in response.json()

def test_login_with_not_verified_user( client_app ):

  create_user = {
    "cargo_id" : 1,
    "password": "1234", 
    "name": "ValidCreate",
    "email": "validCreate@email.com", 
  }
  response = client_app.post("/user/add", json=create_user)

  assert response.is_success
  assert response.json().get("error") == False

  invalid_user = {"username" : "validCreate@email.com", "password": "1234"}
  response = client_app.post("/auth/login",data=invalid_user)

  response_json = response.json()

  assert not response.is_success
  assert "error" in response_json
  assert not response_json.get("error")

def test_login_with_valid_user( client_app ):

  valid_user = {"username" : "teste@email.com", "password": "1234"}
  response = client_app.post("/auth/login",data=valid_user)

  response_json = response.json()
  
  assert "access_token" in response_json
  assert "refresh_token" in response_json
  assert "token_type" in response_json

  assert response_json.get("token_type") == "Bearer"

