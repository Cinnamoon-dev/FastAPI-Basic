from tests.conftest import client_app, test_db


def test_read_all(client_app, test_db):
    response = client_app.get("/user/all")
    assert response.is_success == True
    assert type(response.json()["itens"]) == list

def test_create_user(client_app, test_db):
    create_user = {"email": "test@email.com", "password": "1234", "name": "test"}
    response = client_app.post("/user/add", json=create_user)
    print(response.json())
    assert response.is_success == True
    assert response.json().get("error") == False