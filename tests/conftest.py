import pytest
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from task_tracker_api.main import app 
from task_tracker_api.database import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

@pytest.fixture()
def db_session():
    # Membuat schema baru untuk setiap test
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

     # Membersihkan schema setelah test selesai
    SQLModel.metadata.drop_all(engine)

@pytest.fixture()
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
