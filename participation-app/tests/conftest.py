import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.infrastructure.database.database import Base, get_db
from app.core.security import get_current_user, require_manager, AuthenticatedUser

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]

@pytest.fixture
def override_manager(client):
    def mock_manager():
        return AuthenticatedUser(id="manager_1", roles=["MANAGER"])
    app.dependency_overrides[require_manager] = mock_manager
    yield
    del app.dependency_overrides[require_manager]

@pytest.fixture
def override_user(client):
    def mock_user():
        return AuthenticatedUser(id="user_1", roles=["PARTICIPANT"])
    app.dependency_overrides[get_current_user] = mock_user
    yield
    del app.dependency_overrides[get_current_user]
