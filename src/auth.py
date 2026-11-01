"""
Authentication module.

Provides the login() function used to validate user credentials
against a simple in-memory credential store.
"""

# Demo credential store (username -> password)
_CREDENTIALS: dict[str, str] = {
    "admin": "admin123",
    "surya": "teja@2026",
    "testuser": "password",
}


def login(username: str, password: str) -> bool:
    """
    Authenticate a user with the given username and password.

    Parameters
    ----------
    username : str
        The account username.
    password : str
        The account password.

    Returns
    -------
    bool
        True  – credentials are valid and non-empty.
        False – credentials are empty, missing, or incorrect.
    """
    if not username or not password:
        return False

    return _CREDENTIALS.get(username) == password
# Experiment 1 comment — auth module updated
