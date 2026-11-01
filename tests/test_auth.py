"""
Tests for the Authentication module (src/auth.py).
"""

import pytest
from src.auth import login


class TestLogin:
    """Unit tests for login()."""

    # ------------------------------------------------------------------
    # Valid credential tests
    # ------------------------------------------------------------------

    def test_valid_login_admin(self):
        """Correct credentials for 'admin' should return True."""
        assert login("admin", "admin123") is True

    def test_valid_login_surya(self):
        """Correct credentials for 'surya' should return True."""
        assert login("surya", "teja@2026") is True

    # ------------------------------------------------------------------
    # Invalid credential tests
    # ------------------------------------------------------------------

    def test_invalid_login_wrong_password(self):
        """Wrong password must return False."""
        assert login("admin", "wrongpassword") is False

    def test_invalid_login_unknown_user(self):
        """Unknown username must return False."""
        assert login("nobody", "password") is False

    def test_invalid_login_empty_username(self):
        """Empty username must be rejected (return False)."""
        assert login("", "admin123") is False

    def test_invalid_login_empty_password(self):
        """Empty password must be rejected (return False)."""
        assert login("admin", "") is False
