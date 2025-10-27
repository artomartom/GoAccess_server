import os

from io import TextIOWrapper as file_handle

from fastapi import FastAPI, Request, Query
import aiofiles
import re



def filter_file_in_batches(input_file_handle:file_handle , output_file_handle:file_handle, regex: str, batch_size: int = 10000) -> None:

    lines:int=0
    batchs:int=0
    matches:int=0
    while True:
        batch_empty:bool=False
        filtered_data:str=''
        for _ in range(batch_size):
            line = input_file_handle.readline()
            lines+= 1
            if not line:
                batch_empty =True
                break
            if re.search(regex, line):
                filtered_data += line
                matches+=1

        batchs+=1

        if filtered_data:
            output_file_handle.write(filtered_data)

        if batch_empty:
            break

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
    #with open("/home/kiwi/logs/test.log", 'r') as f:
    #    db = Database()
    #    id = "sxgsdgdfgsdg"[0:20]
    #    assert db.id_exists(id) == False
    #    data = f.read()
    #    db.add_logfile(id,data)
    #    assert db.id_exists(id) == True
    #    data_res = db.get_logfile(id)
    #
    #    if data_res  == data and db.id_exists(id):
    #        print("OK")
    #
    #    os.remove(f"{os.getcwd()}/data/sxgsdgdfgsdg")

    inpt = open("/opt/goAccess_server/log", 'r')
    outpt = open("/opt/goAccess_server/filter", 'w')

    filter_file_in_batches(inpt, outpt,'8.217.208.28',100 )