from datetime import datetime, timedelta
from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from loguru import logger
from passlib.context import CryptContext
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.core.config import setting
from app.core.exception_handler import CustomException
from app.helpers.enum import ErrorMessage, TokenType

# from app.db.schemas import auth

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


# def get_user_by_id(user_id: int, session: Session):
#     user = (
#         session.query(models.User.id, models.User.email)
#         .filter(
#             and_(
#                 models.User.id == user_id, models.User.status == CommonStatus["ACTIVE"]
#             )
#         )
#         .first()
#     )

#     if user is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
#         )

#     return user


def generate_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update(
        {
            "expire": expire.strftime("%Y-%m-%d %H:%M:%S"),
            "token_type": TokenType.ACCESS_TOKEN,
            "iat": datetime.utcnow(),
        }
    )

    encoded_jwt = jwt.encode(to_encode, setting.SECRET_KEY, setting.ALGORITHM)

    return encoded_jwt


def generate_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update(
        {
            "expire": expire.strftime("%Y-%m-%d %H:%M:%S"),
            "token_type": TokenType.REFRESH_TOKEN,
            "iat": datetime.utcnow(),
        }
    )

    encoded_jwt = jwt.encode(to_encode, setting.SECRET_KEY, setting.ALGORITHM)

    return encoded_jwt


def verify_token_access(token: str, credentials_exception):
    try:
        payload: Any = jwt.decode(token, setting.SECRET_KEY, setting.ALGORITHM)
        token_type: TokenType = payload.get("token_type")
        # checking token expire
        if (
            datetime.strptime(payload.get("expire"), "%Y-%m-%d %H:%M:%S")
            < datetime.utcnow()
        ):
            raise CustomException(
                message=ErrorMessage.Token_Expire,
                http_code=status.HTTP_401_UNAUTHORIZED,
            )

        if token_type != TokenType.ACCESS_TOKEN:
            raise CustomException(
                http_code=status.HTTP_401_UNAUTHORIZED,
                message=ErrorMessage.Unauthorized,
            )

    except JWTError as e:
        logger.error(e)
        raise credentials_exception

    return True


def verify_refresh_access(token: str, credentials_exception):
    try:
        payload: Any = jwt.decode(token, setting.SECRET_KEY, setting.ALGORITHM)
        token_type: TokenType = payload.get("token_type")
        # checking token expire
        if (
            datetime.strptime(payload.get("expire"), "%Y-%m-%d %H:%M:%S")
            < datetime.utcnow()
        ):
            raise CustomException(
                message=ErrorMessage.Token_Expire,
                http_code=status.HTTP_401_UNAUTHORIZED,
            )

        if token_type != TokenType.REFRESH_TOKEN:
            raise CustomException(
                http_code=status.HTTP_401_UNAUTHORIZED,
                message=ErrorMessage.Unauthorized,
            )

    except JWTError as e:
        logger.error(e)
        raise credentials_exception

    return True


# def get_current_user(
#     token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
# ):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not Validate Credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     payload = verify_token_access(token, credentials_exception, db)

#     user = get_user_by_id(payload["user_id"], db)
#     return user


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(non_hashed_pass, hashed_pass):
    return pwd_context.verify(non_hashed_pass, hashed_pass)
