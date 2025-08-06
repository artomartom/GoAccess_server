from subprocess import PIPE, Popen, CompletedProcess
import subprocess
 
import  settings  

from  format_parser import Format 

from utility import   logger
import os
import uuid

def get_report_url(filename):
    return f"{ settings.HOSTNAME}/{filename}"
 
     
def new_report_id():
    return  uuid.uuid4().hex

 
def get_format(log_strings : str   ) -> Format:
     
    best_sample_line: str = ""
    best_sample_line_num: int = 0
    best_sample_count: int  = 99
    for line_num in range(len(log_strings)):    
        line = log_strings[line_num]
        count = line.count('"-"')
        if best_sample_count > count:
            best_sample_line_num = line_num
            best_sample_line = line
            best_sample_count = count
    logger(f"best sample line{best_sample_line}")
    return  Format(best_sample_line)

def run_goaccess(  data : str) -> str: 
     
    format = get_format(data.split('\n', 10))
        
    if format.name == "unknown format":
       raise Exception( "unknown format")
	
    logger(f"trying format {format.name }")
    import tempfile
    
    with tempfile.NamedTemporaryFile() as tmp:
        tmp.write(data.encode())
        
        args=  ["goaccess",tmp.name,    "-a", 
                "--log-format", f'{format.log_format}',
                f"--date-format={format.date_format}",  
                f"--time-format={format.time_format }"] 
     
        result =  subprocess.run(
            args, 
            capture_output=True,
            encoding="utf-8",
            text=True
        )
 
    
    if result.returncode != 0:
        raise Exception( result.stderr)
    
    return result.stdout   
    
 
