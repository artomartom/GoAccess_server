import os 


from fastapi import FastAPI, Request, Query
import aiofiles    
class Database:
    
    dir = f"{os.getcwd()}/data"

    def __init__(self):
        if os.path.exists(self.dir) == False:
            os.makedirs(self.dir) 
    
    async def add_logfile_async(self,filename:str,request:Request)-> None:
        async with aiofiles.open(f"{self.dir}/{filename}", 'wb') as file:
            async for chunk in request.stream():
                await file.write(chunk)
        
        
    def add_logfile(self,filename:str,data:bytes)-> None:
        with open(f"{self.dir}/{filename}" , 'wb') as file: 
            file.write(data)
        
    def id_exists(self,id:str )-> str:
        return os.path.isfile(f"{self.dir}/{id}")
        
    def get_logfile(self,id:str ) -> str: 
        
        with  open(f"{self.dir}/{id}" , 'r') as file: 
            return  file.read()   
            #return   '113.168.228.73 - - [08/Jul/2025:00:00:23 +0300] "GET ?orderby=price-desc&availability=in_stock&filter_automatic-winding=no-power-reserve-38-hours&query_type_automatic-winding=or&filter_movement=2414a,2414,2432-01,2431-01,2416 HTTP/1.1" 400 157 "-" "-"'
            
      


if __name__ == '__main__':
    
    #with open("/home/kiwi/logs/nasha-set_access.log-20250718", 'r') as f:
    with open("/home/kiwi/logs/test.log", 'r') as f:
        db = Database()
        id = "sxgsdgdfgsdg"[0:20]
        assert db.id_exists(id) == False
        data = f.read()
        db.add_logfile(id,data)
        assert db.id_exists(id) == True
        data_res = db.get_logfile(id)
        
        if data_res  == data and db.id_exists(id):
            print("OK")
            
        os.remove(f"{os.getcwd()}/data/sxgsdgdfgsdg")