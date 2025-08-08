import redis

from settings import CACHE_SRV, CACHE_PORT, DEBUG

 
class Cache_Server:
    
    redis : redis.client.Redis   
    def __init__(self):
        
        
        self.redis = redis.Redis(host=CACHE_SRV, port=CACHE_PORT, db=0)
        if DEBUG:
            assert  self.redis.ping() == True

    def get(self,key: str):
        return self.redis.get(key)
    def set(self,key: str, html : str):
        return self.redis.set(key,html)

if __name__ == '__main__':
    
    ca = Cache_Server()
    
    assert ca.get("test") == None
    
    ca.set("test","""<!DOCTYPE html>
    <html>
    <body>

    <h1>My First Heading</h1>
    <p>My first paragraph.</p>

    </body>
    </html>""") 
    print(ca.get("test"))

    assert ca.get("test") == b'<!DOCTYPE html>\n    <html>\n    <body>\n\n    <h1>My First Heading</h1>\n    <p>My first paragraph.</p>\n\n    </body>\n    </html>'
    