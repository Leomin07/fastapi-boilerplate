"""
SQL Alchemy models declaration.
https://docs.sqlalchemy.org/en/14/orm/declarative_styles.html#example-two-dataclasses-with-declarative-table
Dataclass style for powerful autocompletion support.

https://alembic.sqlalchemy.org/en/latest/tutorial.html
Note, it is used by alembic migrations logic, see `alembic/env.py`

Alembic shortcuts:
# create migration
alembic revision --autogenerate -m "migration_name"

# apply all migrations
alembic upgrade head

# downgrade migration 
alembic downgrade -1

# history migrations
alembic history
"""
from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime, SmallInteger

from app.db.init_db import Base
from app.helpers.enum import CommonStatus


class ParentModel(Base):
    __abstract__ = True

    id = Column(BigInteger, primary_key=True, index=True)
    status = Column(
        SmallInteger,
        default=CommonStatus.ACTIVE,
        comment="INACTIVE = 0, ACTIVE = 1, PENDING = 2",
        nullable=False,
    )
    createdAt = Column(DateTime, nullable=False, default=datetime.utcnow)
    updatedAt = Column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
