from redis import Redis

from app.core.config import setting

redis_client = Redis(host=setting.REDIS_HOST, port=setting.REDIS_PORT)


def set_cache(key, value, ttl: int | None = 60):
    redis_client.set(key, value, ex=ttl)


def get_cache(key):
    return redis_client.get(key)
