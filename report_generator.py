import subprocess

 
import  settings  

from  format_parser import Format 

from utility import   logger

def get_report_url(filename):
    return f"{ settings.HOSTNAME}/{filename}"
import uuid
 
import hashlib
import datetime

def new_report_id():
     
    #formatted_date =  datetime.datetime.now().strftime("%H:%M:%S_%y%m%d") 
    #formatted_date =  datetime.datetime.now().strftime("%H%M%S%f%Y") 
    #hash =  hashlib.sha256(formatted_date.encode()).hexdigest() 
  
    #return str(hash[:20])
    return  uuid.uuid4().hex

 
def get_format(log_strings   ):
     
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
    #print(f"best sample found  at line {best_sample_line_num}")
    return  Format(best_sample_line)

def run_goaccess(  data): 
    
    format = get_format(data.split('\n', 10))
        
        
    if format.name == "unknown format":
       raise Exception( "unknown format")
    
    args=  ['goaccess',  "-a", #"-o", f"{settings.REPORTS_DIR}/{report_name}",
            "--log-format", f'{format.log_format}',
            f"--date-format={format.date_format}",  
            f"--time-format={format.time_format }"] 
    
    logger(f"trying format {format.name }")
    result =  subprocess.run(
        args,
        input= data,
        capture_output=True,
        encoding="utf-8",
        text=True
    )
    
    
    if result.returncode != 0:
        raise Exception( result.stderr)
    
    return result 
    
    #print (f"running goaccess")
    #print (f"file path {file_path}")
    #print (f"report path  {settings.REPORTS_DIR}/{report_name}")
    
