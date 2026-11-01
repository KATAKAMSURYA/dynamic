"""
Tests for the Payment module (src/payment.py).
"""

import pytest
from src.payment import process_payment


class TestProcessPayment:
    """Unit tests for process_payment()."""

    # ------------------------------------------------------------------
    # Valid payment tests
    # ------------------------------------------------------------------

    def test_valid_payment_standard(self):
        """A typical positive amount within limits should return True."""
        assert process_payment(500.00) is True

    def test_valid_payment_minimum(self):
        """The configured minimum boundary value should be accepted."""
        assert process_payment(0.01) is True

    def test_valid_payment_maximum(self):
        """The configured maximum boundary value should be accepted."""
        assert process_payment(10_000.00) is True

    # ------------------------------------------------------------------
    # Invalid payment tests
    # ------------------------------------------------------------------

    def test_invalid_payment_zero(self):
        """Zero is not a valid payment amount."""
        assert process_payment(0) is False

    def test_invalid_payment_negative(self):
        """Negative amounts must be rejected."""
        assert process_payment(-50.00) is False

    def test_invalid_payment_exceeds_limit(self):
        """Amounts above the upper limit must be rejected."""
        assert process_payment(10_001.00) is False

