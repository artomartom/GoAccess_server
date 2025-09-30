import os 


from fastapi import FastAPI, Request, Query
import aiofiles    
import re


def match_regex(match: str, data: list[str])-> str:
        
    new_data:str="" 
    for line in data:
        if re.search(match, line):
            new_data+=line  
            new_data+='\n' 
    return  new_data
 
 
def filter_file_in_batches(input_file_handle, output_file_handle: str, regex: str, batch_size: int = 10000) -> None:
   
    while True:
        batch = []
        for _ in range(batch_size):
            line = input_file_handle.readline()
            if not line:   
                break
            batch.append(line)
        
        if not batch:
            break
        
        filtered_data = match_regex(regex, batch)
        
        if filtered_data:
            output_file_handle.write(filtered_data) 
                
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
        return  open(f"{self.dir}/{id}" , 'r')  
        

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