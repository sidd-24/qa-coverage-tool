"""
Reusable test patterns for common scenarios.
Import these into specific test files.
"""

def assert_valid_token(token: str):
    """Pattern: validate a token looks correct."""
    assert token is not None
    assert len(token) > 10
    assert isinstance(token, str)

def assert_error_response(response: dict, expected_status: int):
    """Pattern: validate an error response shape."""
    assert response["status"] == expected_status
    assert response["error"] is not None

def assert_success_response(response: dict):
    """Pattern: validate a success response shape."""
    assert response["status"] == 200
    assert response["data"] is not None

def build_registration_payload(email: str, password: str) -> dict:
    """Pattern: construct a registration payload."""
    return {"email": email, "password": password}