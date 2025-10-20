import redis

from settings import  Settings
from utility import Logger as log

 
class Cache_Server:
    
    active:bool=True
    
    redis:redis.client.Redis   
    def __init__(self):
        
        if not Settings.cache:
            self.active:bool =False
            return 
        
        try:
            self.redis = redis.Redis(host=Settings.cache_srv, port=Settings.cache_port, db=0)
            self.set('test','testtest')
            _:str = self.get('test')
        except Exception as e:
            log.warn(f"unable to connect to ${Settings.cache_srv}:${Settings.cache_port}.\nCaching diabled")
            self.active = False
            pass  

    def get(self,key: str):
        if not self.active:
            return None
        return self.redis.get(key)
    def set(self,key: str, html : str):
        if not self.active:
            return None
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
    