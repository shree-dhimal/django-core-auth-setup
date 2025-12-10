from django_redis import get_redis_connection

class RedisClient:
    """
    Wrapper over django_redis connection with common helpers.
    from common_core.cache.redis_cache import redis_client
            redis_client.set("count", 10)
            value = redis_client.get("count")
    """

    def __init__(self, alias="default"):
        self.conn = get_redis_connection(alias)

    def set(self, key, value, ttl=None):
        self.conn.set(key, value, ex=ttl)

    def get(self, key):
        return self.conn.get(key)

    def delete(self, key):
        return self.conn.delete(key)

    def incr(self, key, amount=1):
        return self.conn.incr(key, amount)

    def exists(self, key):
        return self.conn.exists(key)

    def expire(self, key, ttl):
        self.conn.expire(key, ttl)

    def ping(self):
        return self.conn.ping()


redis_client = RedisClient()