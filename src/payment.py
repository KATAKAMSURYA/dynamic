"""
Payment processing module.

Provides the process_payment() function that validates and processes
monetary transactions within configured limits.
"""

# Configurable limits
_MIN_AMOUNT: float = 0.01   # exclusive lower bound (must be > 0)
_MAX_AMOUNT: float = 10_000.00  # inclusive upper bound


def process_payment(amount: float) -> bool:
    """
    Process a payment for the given amount.

    Parameters
    ----------
    amount : float
        The payment amount in the local currency unit.

    Returns
    -------
    bool
        True  – the amount is within the valid range and was processed.
        False – the amount is zero, negative, or exceeds the upper limit.
    """
    if not isinstance(amount, (int, float)):
        return False

    return _MIN_AMOUNT <= amount <= _MAX_AMOUNT
