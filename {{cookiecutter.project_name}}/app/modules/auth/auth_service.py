from fastapi import status
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.core.exception_handler import CustomException
from app.core.security import (
    generate_access_token,
    generate_refresh_token,
    hash_password,
    verify_password,
)
from app.helpers.enum import CommonStatus, ErrorMessage, TokenType
from app.models import user_model
from app.modules.auth.auth_sche import (
    login_schema,
    refresh_token_schema,
    register_schema,
)


def check_email_duplicate(email: str, db: Session):
    obj = (
        db.query(user_model.User.id, user_model.User.email)
        .filter_by(email=email)
        .first()
    )

    if obj:
        raise CustomException(
            message=ErrorMessage.Email_Already_Exist,
        )

    return


def check_user_by_id(user_id: int, db: Session):
    user = (
        db.query(user_model.User.id, user_model.User.status)
        .filter(
            and_(
                user_model.User.id == user_id,
                user_model.User.status == CommonStatus.ACTIVE,
            )
        )
        .first()
    )

    if user is None:
        raise CustomException(
            message=ErrorMessage.User_Not_Found,
        )

    return


def check_user_by_email(email: str, db: Session):
    user = (
        db.query(user_model.User.id, user_model.User.email, user_model.User.status)
        .filter(
            and_(
                user_model.User.email == email,
                user_model.User.status == CommonStatus.ACTIVE,
            )
        )
        .first()
    )

    if user is None:
        raise CustomException(
            message=ErrorMessage.User_Not_Found,
        )

    return user


def generate_token(user_id: int):
    # generate_access_token
    access_token = generate_access_token(data={"user_id": user_id})
    # generate_refresh_token
    new_refresh_token = generate_refresh_token(data={"user_id": user_id})

    return {"access_token": access_token, "refresh_token": new_refresh_token}


def register(db: Session, params: register_schema):
    # check email duplicate
    check_email_duplicate(params.email, db)

    # hashed password
    params.password = hash_password(params.password)
    # create new user
    new_user = user_model.User(**params.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = generate_token(int(new_user.id))

    db.query(user_model.User).filter_by(id=new_user.id).update(
        {"refresh_token": token["refresh_token"]}
    )
    db.commit()

    return token


def login(db: Session, params: login_schema):
    user = (
        db.query(user_model.User)
        .filter(
            and_(
                user_model.User.email == params.email,
                user_model.User.status == CommonStatus.ACTIVE,
            )
        )
        .first()
    )

    if user is None:
        raise CustomException(
            message=ErrorMessage.User_Not_Found,
            http_code=status.HTTP_401_UNAUTHORIZED,
        )

    if not verify_password(params.password, user.password) == True:
        raise CustomException(
            message=ErrorMessage.Password_Not_Match,
            http_code=status.HTTP_401_UNAUTHORIZED,
        )

    token = generate_token(int(user.id))

    db.query(user_model.User).filter_by(email=params.email).update(
        {"refresh_token": token["refresh_token"]}
    )
    db.commit()

    return token


def refresh_token(params: refresh_token_schema, db: Session):
    user = (
        db.query(user_model.User)
        .where(user_model.User.refresh_token == params.refresh_token)
        .first()
    )

    if user is None:
        raise CustomException(
            http_code=status.HTTP_401_UNAUTHORIZED, message="Refresh token is expired"
        )

    token = generate_token(int(user.id))

    db.query(user_model.User).filter_by(id=user.id).update(
        {"refresh_token": token["refresh_token"]}
    )
    db.commit()

    return token
