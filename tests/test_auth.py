from tests.conftest import client, test_db

""" Arquivo de teste de autenticação """

def test_add_user_to_login(test_db):
  valid_user_to_add = {"name" : "pedro","email": "teste@email.com", "password": "1234"}
  response = client.post("/user/add", json=valid_user_to_add)

  response_json = response.json()
  assert response.status_code == 200
  assert response_json.get("error") == False


def test_login_with_valid_user(test_db):
  valid_user = {"username" : "pedro@email.com", "password": "1234"}
  response = client.post("/user/add", json=valid_user)
  response = client.post("/auth/login",data=valid_user)

  assert response.status_code == 202
  assert "access_token" in response.json()
  assert "refresh_token" in response.json()

def test_login_with_invalid_user(test_db):
  valid_user = {"username" : "sherek@email.com", "password": "1234"}
  response = client.post("/auth/login",data=valid_user)

  assert response.status_code != 202
  assert "access_token" not in response.json()
  assert "refresh_token" not in response.json()
  assert response.is_success == False