from datetime import datetime, timedelta, timezone

import jwt  
from jwt.exceptions import PyJWTError

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from dotenv import load_dotenv

import os

from app.exceptions.auth import InvalidTokenError


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

ISSUER_NAME = os.getenv("ISSUER_NAME")

ALGORITHM = os.getenv("ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
)


ph = PasswordHasher()


def hash_password(password: str) -> str:
    return ph.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    try:
        return ph.verify(
            hashed_password,
            plain_password
        )
    
    except VerifyMismatchError:
        return False
    

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "iss": ISSUER_NAME,
        "token_type": "access"
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def verify_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        return payload
    
    except PyJWTError:
        raise InvalidTokenError()