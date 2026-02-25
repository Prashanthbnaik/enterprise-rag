import redis
from app.core.config import REDIS_HOST, REDIS_PORT

try:
    redis_client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        decode_responses=True
    )

    redis_client.ping()

except Exception:
    redis_client = None