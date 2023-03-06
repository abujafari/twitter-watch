import os

import redis

pool = redis.ConnectionPool(
    host=os.environ.get("REDIS_HOST", "localhost"),
    port=os.environ.get("REDIS_PORT", "6379"),
    db=os.environ.get("REDIS_DB", "1"),
    decode_responses=True
)


def get_redis_connection():
    return redis.StrictRedis(connection_pool=pool)
