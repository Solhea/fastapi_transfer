import os
from dotenv import load_dotenv
load_dotenv()

from passlib.context import CryptContext
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


from core.cruds.user_crud import get_user_by_username
from core.utils.helpers import get_db

def hash_password(password):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expires_delta = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
    if expires_delta:
        expire = datetime.utcnow() + timedelta(minutes=int(expires_delta))
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.environ.get("SECRET_KEY"), algorithm=os.environ.get("ALGORITHM"))
    return encoded_jwt

async def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="/api/auth/login",scheme_name="JWT")), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    signature_expired = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Signature expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.environ.get("SECRET_KEY"), algorithms=os.environ.get("ALGORITHM"))
        username: str = payload["username"]
        if username is None:
            raise credentials_exception
        token_data = {"username": username}
    except JWTError as e:
        if str(e) == "Signature has expired.":
            raise signature_expired
        raise credentials_exception
    user = get_user_by_username(db, username=token_data["username"])
    if user is None:
        raise credentials_exception
    return user
