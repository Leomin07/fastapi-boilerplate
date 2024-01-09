import json
from loguru import logger
from app.core import config
from app.core.caching import set_cache
from app.db.models import member_model
from sqlalchemy.orm import Session

from app.helpers.utils import generate_key


def get_profile(db: Session, member_id: int):
    member = db.query(member_model.Member).filter_by(id=member_id).first()
    return member
