from datetime import datetime, timedelta 
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "secret_key_auth"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated = "auto"
)

def hash_password(password : str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def create_access_tokken(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp" : expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)

def decode_access_token(token : str):
    try: 
        return jwt.decode(token, SECRET_KEY, algorithm=[ALGORITHM])
    except JWTError:
        return None