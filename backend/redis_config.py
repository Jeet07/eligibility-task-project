import redis
import json
import logging

logger = logging.getLogger(__name__)

class RedisCache:
    def __init__(self, host='redis', port=6379, db=0):
        self.client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5
        )
    
    def get(self, key: str):
        try:
            value = self.client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Redis get error: {e}")
            return None
    
    def set(self, key: str, value, ttl: int = 3600):
        try:
            self.client.setex(key, ttl, json.dumps(value))
            return True
        except Exception as e:
            logger.error(f"Redis set error: {e}")
            return False
    
    def delete(self, key: str):
        try:
            self.client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Redis delete error: {e}")
            return False
    
    def delete_pattern(self, pattern: str):
        try:
            keys = self.client.keys(pattern)
            if keys:
                return self.client.delete(*keys)
            return 0
        except Exception as e:
            logger.error(f"Redis delete pattern error: {e}")
            return 0

task_cache = RedisCache(host='redis', port=6379, db=0)
eligibility_cache = RedisCache(host='redis', port=6379, db=1)
