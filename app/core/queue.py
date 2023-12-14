"""
https://python-rq.org/docs/

rq worker --with-scheduler
"""

from redis import Redis
from rq import Queue

from app.core.config import setting

redis_conn = Redis(host=setting.REDIS_HOST, port=setting.REDIS_PORT)

queue = Queue(connection=redis_conn)
