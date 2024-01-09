from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_read_all():
    response = client.get("/user/all")
    assert response.is_success == True
    assert type(response.json()["itens"]) == list