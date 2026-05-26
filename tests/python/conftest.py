import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import pytest

@pytest.fixture
def mock_user():
    return {"email": "test@example.com", "password": "securepass123"}

@pytest.fixture
def mock_auth_token():
    return "mock-jwt-token-abc123"

@pytest.fixture
def mock_api_response():
    def _response(status=200, data=None, error=None):
        return {"status": status, "data": data or {}, "error": error}
    return _response