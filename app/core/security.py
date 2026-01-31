from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Bcrypt has a maximum password length of 72 bytes
    # Truncate the password to avoid ValueError
    truncated_password = plain_password.encode("utf-8")[:72].decode(
        "utf-8", errors="ignore"
    )
    return pwd_context.verify(truncated_password, hashed_password)


def get_password_hash(password: str) -> str:
    # Bcrypt has a maximum password length of 72 bytes
    # Truncate the password to avoid ValueError
    truncated_password = password.encode("utf-8")[:72].decode("utf-8", errors="ignore")
    return pwd_context.hash(truncated_password)
