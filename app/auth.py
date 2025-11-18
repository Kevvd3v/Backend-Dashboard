from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os

PWD_CTX = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

JWT_SECRET = os.getenv("JWT_SECRET", "change_me_in_prod")
JWT_ALG = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  

MAX_PASS_BYTES = 1024  

def hash_password(password: str) -> str:
    if password is None:
        raise ValueError("Password empty")
    pw = str(password)
    if len(pw.encode("utf-8")) > MAX_PASS_BYTES:
        pw = pw.encode("utf-8")[:MAX_PASS_BYTES].decode("utf-8", errors="ignore")
    return PWD_CTX.hash(pw)

def verify_password(password: str, hashed: str) -> bool:
    if password is None:
        return False
    pw = str(password)
    if len(pw.encode("utf-8")) > MAX_PASS_BYTES:
        pw = pw.encode("utf-8")[:MAX_PASS_BYTES].decode("utf-8", errors="ignore")
    try:
        return PWD_CTX.verify(pw, hashed)
    except Exception:
        return False

def create_access_token(subject: str, expires_delta: int = None):
    expire = datetime.utcnow() + timedelta(minutes=(expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = {"exp": expire, "sub": str(subject)}
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALG)

def decode_access_token(token: str):
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
