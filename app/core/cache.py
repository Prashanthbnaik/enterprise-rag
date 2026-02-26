import os
import redis

REDIS_URL = os.getenv("REDIS_URL")

try:
    if REDIS_URL:
        redis_client = redis.from_url(
            REDIS_URL,
            decode_responses=True
        )
        redis_client.ping()
    else:
        redis_client = None

except Exception:
    redis_client = None