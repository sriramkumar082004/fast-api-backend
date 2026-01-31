from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _truncate_password(password: str) -> str:
    """
    Safely truncate password to 72 bytes for bcrypt compatibility.
    Ensures we don't cut in the middle of a multi-byte UTF-8 character.
    """
    encoded = password.encode("utf-8")
    if len(encoded) <= 72:
        return password

    # Truncate to 72 bytes, then find the last valid UTF-8 character boundary
    truncated = encoded[:72]
    # Decode with 'ignore' to drop any incomplete character at the end
    # Then re-encode to ensure consistency
    result = truncated.decode("utf-8", errors="ignore")

    # Double-check the result is still within 72 bytes
    while len(result.encode("utf-8")) > 72:
        result = result[:-1]

    return result


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    truncated_password = _truncate_password(plain_password)
    return pwd_context.verify(truncated_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    truncated_password = _truncate_password(password)
    return pwd_context.hash(truncated_password)
