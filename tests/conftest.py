import pytest
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.database import Base, get_db,SQLALCHEMY_DATABASE_URL


@pytest.fixture(scope="session")
def _engine():
    return create_engine(SQLALCHEMY_DATABASE_URL)

@pytest.fixture(scope="function")
def tables(_engine):
    Base.metadata.create_all(bind=_engine)
    yield
    Base.metadata.drop_all(bind=_engine)

@pytest.fixture(scope="function")
def client_app(_engine, tables):
    connection = _engine.connect()
    transaction = connection.begin()

    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)

    def _override_get_db():
        _db = TestSessionLocal()
        try:
            yield _db
        finally:
            _db.close()

    app.dependency_overrides[get_db] = _override_get_db
    client = TestClient(app)
    yield client

    TestSessionLocal.close_all()
    transaction.rollback()
    connection.close()