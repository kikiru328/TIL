import pytest

from fastapi.testclient import TestClient
from main import app

# fixture
@pytest.fixture
def client(): #this will be fix in test code
    return TestClient(app=app)