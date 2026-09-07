from __future__ import annotations

from passlib.context import CryptContext
from passlib.exc import UnknownHashError


_PASSWORD_CONTEXT = CryptContext(
    schemes=[
        "bcrypt",
        "pbkdf2_sha256",
    ],
    deprecated="auto",
)

_SUPPORTED_SCHEMES = frozenset(
    {
        "bcrypt",
        "pbkdf2_sha256",
    }
)


def verify_password(
    plain_password: str,
    stored_password: str,
) -> bool:
    """
    Verify an AIHA canonical user password without mutating stored credentials.

    Supported canonical formats:
    - bcrypt
    - passlib pbkdf2_sha256

    Unknown, malformed, empty, or unsupported values fail closed.
    """

    if not isinstance(plain_password, str):
        return False

    if not isinstance(stored_password, str):
        return False

    if not plain_password:
        return False

    if not stored_password:
        return False

    try:
        scheme = _PASSWORD_CONTEXT.identify(
            stored_password
        )
    except Exception:
        return False

    if scheme not in _SUPPORTED_SCHEMES:
        return False

    try:
        return bool(
            _PASSWORD_CONTEXT.verify(
                plain_password,
                stored_password,
            )
        )
    except (
        ValueError,
        TypeError,
        UnknownHashError,
    ):
        return False
