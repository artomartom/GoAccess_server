import redis

from settings import  Settings

 
class Cache_Server:
    
    redis:redis.client.Redis   
    
    def __init__(self):
        
        if not Settings.cache:
            return 
        
        try:
            self.redis = redis.Redis(host=Settings.cache_srv, port=Settings.cache_port, db=0)
        except Exception as e:
            Settings.cache = False
            pass  
        

    def get(self,key: str):
        if not Settings.cache:
            return None
        return self.redis.get(key)
    def set(self,key: str, html : str):
        if not Settings.cache:
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
    