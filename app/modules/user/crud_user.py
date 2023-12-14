# from fastapi import HTTPException, status
# from sqlalchemy import and_
# from sqlalchemy.orm import Session

# from app.core.dict import CommonStatus
# from app.core.security import hash_password
# from app.db import models
# from app.db.schemas.auth import user_register


# def check_duplicate_email(email: str, session: Session):
#     user = (
#         session.query(models.User.id, models.User.email).filter_by(email=email).first()
#     )
#     if user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
#         )

#     return


# def register(session: Session, params: user_register):
#     # check email
#     check_duplicate_email(params.email, session)

#     # hash password
#     hashed_pass = hash_password(params.password)

#     # create new user
#     params.password = hashed_pass
#     new_user = models.User(**params.dict())
#     session.add(new_user)
#     session.commit()
#     session.refresh(new_user)

#     return new_user


# def check_user_found(session: Session, email: str):
#     user = (
#         session.query(
#             models.User.id, models.User.email, models.User.status, models.User.password
#         )
#         .filter(
#             and_(
#                 models.User.email == email, models.User.status == CommonStatus["ACTIVE"]
#             )
#         )
#         .first()
#     )

#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail="User not found"
#         )

#     return user
