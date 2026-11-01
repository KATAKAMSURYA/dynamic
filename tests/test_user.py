"""
Tests for the User Management module (src/user.py).
"""

import pytest
from src.user import create_user


class TestCreateUser:
    """Unit tests for create_user()."""

    # ------------------------------------------------------------------
    # Valid user creation tests
    # ------------------------------------------------------------------

    def test_valid_user_returns_dict(self):
        """Valid name and e-mail should return a dict with those keys."""
        result = create_user("Katakam Surya Teja", "surya@example.com")
        assert result == {"name": "Katakam Surya Teja", "email": "surya@example.com"}

    def test_valid_user_strips_whitespace(self):
        """Leading/trailing whitespace in inputs should be stripped."""
        result = create_user("  Alice  ", "  alice@test.org  ")
        assert result == {"name": "Alice", "email": "alice@test.org"}

    # ------------------------------------------------------------------
    # Invalid user creation tests
    # ------------------------------------------------------------------

    def test_invalid_user_empty_name(self):
        """Empty name must return None."""
        assert create_user("", "valid@example.com") is None

    def test_invalid_user_bad_email(self):
        """Malformed e-mail must return None."""
        assert create_user("Bob", "not-an-email") is None

    def test_invalid_user_empty_email(self):
        """Empty e-mail must return None."""
        assert create_user("Charlie", "") is None
