from subprocess import PIPE, Popen, CompletedProcess
import subprocess
 
import  settings  

from  format_parser import Format, get_format

from utility import   logger
import os
import uuid
import tempfile

def get_report_url(filename):
    return f"{ settings.HOSTNAME}/{filename}"
 
def new_report_id():
    return  uuid.uuid4().hex

def run_goaccess(  data : str) -> str: 
     
    format = get_format(data.split('\n', 10))
        
    if format.name == "unknown format":
       raise Exception( "unknown format")
	
    logger(f"trying format {format.name }")
    
    with tempfile.NamedTemporaryFile('wb') as tmp:
        tmp.write(data.encode())
        
        args=  ["goaccess",tmp.name,    "-a", 
                "--log-format", f'{format.log_format}',
                f"--date-format={format.date_format}",  
                f"--time-format={format.time_format }"] 
     
        result = subprocess.run(
            args, 
            capture_output=True 
        )
    
    if result.returncode != 0:
        raise Exception( result.stderr)
    
    return result.stdout   
    
 
