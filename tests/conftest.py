import pytest
from fastapi.testclient import TestClient
from mongomock import MongoClient
from db.session import get_db
from main import app

@pytest.fixture
def mock_mongo():
    client = MongoClient()
    db = client['testdb']
    yield db
    
@pytest.fixture(autouse=True)
def override_db_dependency(mock_mongo):
    def _get_db_override():
        return mock_mongo
    app.dependency_overrides[get_db] = _get_db_override
    yield
    app.dependency_overrides.clear()

@pytest.fixture
def test_client():
    return TestClient(app)