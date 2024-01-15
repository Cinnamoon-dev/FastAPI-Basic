from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.database import SQLALCHEMY_DATABASE_URL


client = TestClient(app)

engine = create_engine( 
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_read_all():
    response = client.get("/user/all")
    assert response.is_success == True
    assert type(response.json()["itens"]) == list