import redis

from settings import Settings

class Cache_Server:


    redis:redis.client.Redis

    def __init__(self):
        addr, port = tuple(Settings.cache_server.split(":",1))
        self.redis = redis.Redis(host=addr, port=port, db=0)

    def get(self,key: str):
        return self.redis.get(key)
    def set(self,key: str, html : str):
        return self.redis.set(key,html)
