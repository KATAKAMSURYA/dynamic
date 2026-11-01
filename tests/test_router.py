"""
Unit tests for the Dynamic Test-Subset Router (router/test_router.py).

Tests the select_tests() routing logic across the four key scenarios
defined in the assignment specification.
"""

import pytest
from router.test_router import select_tests, normalise, FULL_SUITE, MODULE_TO_TEST


class TestSelectTests:
    """Tests for the select_tests() routing function."""

    # ------------------------------------------------------------------
    # Scenario 1 – Single known module: Authentication
    # ------------------------------------------------------------------

    def test_auth_change_maps_to_auth_tests(self):
        """
        Changing only src/auth.py must route exclusively to
        tests/test_auth.py.
        """
        result = select_tests(["src/auth.py"])
        assert result == ["tests/test_auth.py"], (
            f"Expected ['tests/test_auth.py'], got {result!r}"
        )

    # ------------------------------------------------------------------
    # Scenario 2 – Multiple known modules
    # ------------------------------------------------------------------

    def test_multiple_module_changes_map_to_multiple_tests(self):
        """
        Changing src/auth.py and src/payment.py must route to both
        tests/test_auth.py and tests/test_payment.py (sorted).
        """
        result = select_tests(["src/auth.py", "src/payment.py"])
        assert result == ["tests/test_auth.py", "tests/test_payment.py"], (
            f"Expected both auth and payment test files, got {result!r}"
        )

    # ------------------------------------------------------------------
    # Scenario 3 – Unknown / shared file → full-suite fallback
    # ------------------------------------------------------------------

    def test_unknown_file_triggers_full_suite_fallback(self):
        """
        Changing a file not in MODULE_TO_TEST (e.g. requirements.txt)
        must trigger the full-suite fallback (tests/).
        """
        result = select_tests(["requirements.txt"])
        assert result == [FULL_SUITE], (
            f"Expected full-suite fallback [{FULL_SUITE!r}], got {result!r}"
        )

    # ------------------------------------------------------------------
    # Scenario 4 – Empty change set → full-suite fallback
    # ------------------------------------------------------------------

    def test_empty_changeset_triggers_full_suite_fallback(self):
        """
        An empty list of changed files must trigger the full-suite
        fallback (tests/) — never silently skip tests.
        """
        result = select_tests([])
        assert result == [FULL_SUITE], (
            f"Expected full-suite fallback [{FULL_SUITE!r}], got {result!r}"
        )


class TestNormalise:
    """Tests for the normalise() path helper."""

    def test_strips_leading_dot_slash(self):
        assert normalise("./src/auth.py") == "src/auth.py"

    def test_converts_backslash_to_forward_slash(self):
        assert normalise("src\\payment.py") == "src/payment.py"

    def test_already_clean_path_unchanged(self):
        assert normalise("src/user.py") == "src/user.py"

    def test_combined_backslash_and_dot_slash(self):
        assert normalise(".\\src\\auth.py") == "src/auth.py"
