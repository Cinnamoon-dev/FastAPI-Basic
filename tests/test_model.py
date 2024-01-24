"""
    Arquivo de testes de usuários.
"""


def test_read_all_but_not_logged_in_app( client_app ):
    response = client_app.get("/user/all")
    
    assert not response.is_success
    assert "detail" in response.json()
    assert response.status_code == 401 # not authenticated

def test_create_valid_user( client_app ):
    create_user = {
       "cargo_id" : 1,
       "password": "1234", 
       "name": "ValidCreate",
       "email": "validCreate@email.com", 
    }
    response = client_app.post("/user/add", json=create_user)

    assert response.is_success
    assert response.json().get("error") == False

def test_add_user_with_email_repeated( client_app ):

  valid_user_to_add = {
    "cargo_id" : 1,
    "name" : "pedro",
    "password": "1234",
    "email": "teste@email.com", 
  }
  response = client_app.post("/user/add", json=valid_user_to_add)
  response_json = response.json()

  assert response.status_code == 409
  assert "error" in response_json
  assert "message" in response_json
  assert response_json.get("error") == True