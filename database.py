import os
import regex as re

from io import TextIOWrapper as file_handle

from fastapi import Request
import aiofiles



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
        
    output_file_handle.flush()

class Database:

    dir = f"{os.getcwd()}/data"

    def __init__(self):
        if os.path.exists(self.dir) is False:
            os.makedirs(self.dir)

    async def add_logfile_async(self,filename:str,request:Request)-> None:
        async with aiofiles.open(f"{self.dir}/{filename}", 'wb' ) as file:
            async for chunk in request.stream():
                await file.write(chunk)


    def add_logfile(self,filename:str,data:bytes)-> None:
        with open(f"{self.dir}/{filename}" , 'wb' ) as file:
            file.write(data)

    def id_exists(self,file_id:str )-> str:
        return os.path.isfile(f"{self.dir}/{file_id}")

    def get_logfile(self,file_id:str ) -> str:
        return  open(f"{self.dir}/{file_id}" , 'r',encoding='utf-8')

