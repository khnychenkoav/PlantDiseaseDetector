from passlib.context import CryptContext
import hashlib


def get_hashed_path(filename: str) -> str:
    hash_val = hashlib.md5(filename.encode()).hexdigest()
    return f"{hash_val[:2]}/{hash_val[2:4]}/{hash_val[4:6]}"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
