import random
import time
from datetime import timedelta
from redis.exceptions import RedisError
from ..core.redis_client import redis_client

# In-memory fallback for local dev when Redis is unavailable
_mem_store: dict[str, tuple[str, float]] = {}


def _key(phone: str) -> str:
    return f"otp:{phone}"


def generate_and_store_otp(phone: str, ttl_seconds: int = 300) -> str:
    code = f"{random.randint(100000, 999999)}"
    try:
        redis_client.setex(_key(phone), timedelta(seconds=ttl_seconds), code)
    except RedisError:
        _mem_store[_key(phone)] = (code, time.time() + ttl_seconds)
    return code


def verify_otp(phone: str, code: str) -> bool:
    try:
        stored = redis_client.get(_key(phone))
        if stored and stored == code:
            redis_client.delete(_key(phone))
            return True
    except RedisError:
        entry = _mem_store.get(_key(phone))
        if entry:
            val, exp = entry
            if time.time() <= exp and val == code:
                _mem_store.pop(_key(phone), None)
                return True
    return False
