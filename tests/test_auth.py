
""" 
  Arquivo de teste de autenticação.

  PS: Para simular um formdata é necessário passar data no client.post.
      ele simula um formdata que viria do frontend.
"""


def test_login_with_valid_user(client_app):

  valid_user_login = { "username" : "teste@email.com",  "password": "1234" }
  response = client_app.post("/auth/login", data=valid_user_login)
  
  assert response.is_success
  assert "access_token" in response.json()
  assert "refresh_token" in response.json()


def test_login_with_not_found_user(client_app):

  valid_user = {"username" : "sherek@email.com", "password": "1234"}
  response = client_app.post("/auth/login",data=valid_user)

  assert not response.is_success
  assert response.status_code == 404
  assert "access_token" not in response.json()
  assert "refresh_token" not in response.json()

