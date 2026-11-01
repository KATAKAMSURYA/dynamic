"""
User management module.

Provides the create_user() function that validates and creates
a new user record from the supplied name and e-mail address.
"""

import re

# Minimal e-mail pattern: something@something.something
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def create_user(name: str, email: str) -> dict | None:
    """
    Create and return a user record for the given name and e-mail.

    Parameters
    ----------
    name : str
        Full name of the user. Must be a non-empty string.
    email : str
        E-mail address of the user. Must match a basic e-mail pattern.

    Returns
    -------
    dict
        ``{"name": name, "email": email}`` when inputs are valid.
    None
        When any input fails validation.
    """
    if not name or not isinstance(name, str):
        return None

    if not email or not isinstance(email, str):
        return None

    # Strip whitespace first, then validate
    name = name.strip()
    email = email.strip()

    if not name:
        return None

    if not _EMAIL_RE.match(email):
        return None

    return {"name": name, "email": email}
