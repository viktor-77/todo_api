from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

from jose import jwt, JWTError
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str, minutes: int, secret: str,
                        algorithm: str) -> str:
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=minutes)
    to_encode: Dict[str, Any] = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }
    return jwt.encode(to_encode, secret, algorithm=algorithm)


def decode_token(token: str, secret: str, algorithms: List[str]) -> Dict[
    str, Any]:
    return jwt.decode(token, secret, algorithms=algorithms)
