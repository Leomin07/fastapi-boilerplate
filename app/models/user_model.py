from sqlalchemy import Column, String
from app.models.base_model import ParentModel


class User(ParentModel):
    __tablename__ = "users"

    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone = Column(String(255), unique=True, index=True, nullable=True)
    full_name = Column(String(255), unique=True, index=True)
    refresh_token = Column(String(255), nullable=True)
