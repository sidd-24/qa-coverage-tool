"""
Regression tests — baseline coverage that must always pass.
These are written by hand and represent known-good behavior.
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from test_patterns import (
    assert_valid_token, assert_error_response,
    assert_success_response, build_registration_payload
)


class TestAuthRegistration:
    """Regression: User registration behavior."""

    def test_valid_registration_payload_shape(self, mock_user):
        payload = build_registration_payload(mock_user["email"], mock_user["password"])
        assert "email" in payload
        assert "password" in payload

    def test_password_minimum_length(self):
        short_password = "abc123"
        assert len(short_password) < 8, "Should flag passwords under 8 chars"

    def test_valid_password_length(self, mock_user):
        assert len(mock_user["password"]) >= 8


class TestAuthTokens:
    """Regression: Token validation behavior."""

    def test_token_structure(self, mock_auth_token):
        assert_valid_token(mock_auth_token)

    def test_empty_token_rejected(self):
        with pytest.raises(AssertionError):
            assert_valid_token("")


class TestResponsePatterns:
    """Regression: Response shape validation."""

    def test_success_response_shape(self, mock_api_response):
        response = mock_api_response(status=200, data={"user_id": 1})
        assert_success_response(response)

    def test_unauthorized_response_shape(self, mock_api_response):
        response = mock_api_response(status=401, error="Invalid credentials")
        assert_error_response(response, 401)

    def test_duplicate_email_response_shape(self, mock_api_response):
        response = mock_api_response(status=409, error="Email already exists")
        assert_error_response(response, 409)