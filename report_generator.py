from subprocess import PIPE, Popen, CompletedProcess
import subprocess
 
import  settings  

from  format_parser import Format

from utility import Logger as log
import os
import uuid
import tempfile

def get_report_url(filename):
    return f"{ settings.HOSTNAME}/{filename}"
 
def new_report_id():
    return  uuid.uuid4().hex

def run_goaccess(  filename : str, format : Format ) -> str: 
     
    log.verbose(f"trying format {format.name }")
    args=  ["goaccess",filename,    "-a", 
            "--log-format", f'{format.log_format}',
            f"--date-format={format.date_format}",  
            f"--time-format={format.time_format }"] 
    result = subprocess.run(
        args, 
        capture_output=True 
    )
    
    if result.returncode != 0:
        err = result.stderr.decode()
        log.error(err)
        raise Format.Exception('')
    return result.stdout   
    
 
