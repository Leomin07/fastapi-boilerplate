from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.init_db import get_db
from app.modules.auth import auth_service
from app.modules.auth.auth_sche import (
    login_schema,
    refresh_token_schema,
    register_schema,
)

# from app.core import security

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(params: register_schema, session: Session = Depends(get_db)):
    return auth_service.register(session, params)


@router.post("/login", status_code=status.HTTP_200_OK)
def login(
    params: login_schema,
    session: Session = Depends(get_db),
):
    return auth_service.login(session, params)


@router.post("/refresh-token", status_code=status.HTTP_200_OK)
def refresh_token(
    params: refresh_token_schema,
    session: Session = Depends(get_db),
):
    return auth_service.refresh_token(params, session)
