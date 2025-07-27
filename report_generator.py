import subprocess

 
import  settings  

from  format_parser import Format 

from utility import   logger

def get_report_url(filename):
    return f"{ settings.HOSTNAME}/{filename}"

import hashlib
import datetime

def get_report_file_name():
     
    #formatted_date =  datetime.datetime.now().strftime("%H:%M:%S_%y%m%d") 
    formatted_date =  datetime.datetime.now().strftime("%H%M%S%f%Y") 
    hash =  hashlib.sha256(formatted_date.encode()).hexdigest() 
  
    return str(hash[:20])

def run_goaccess( file_path, report_name): 
    
    format : Format
    with open(file_path, 'r') as log_file:
        best_sample_line: str = ""
        best_sample_line_num: int = 0
        best_sample_count: int  = 99
        for line_num in range(10):    
            line = log_file.readline()
            count = line.count('"-"')
            if best_sample_count > count:
                best_sample_line_num = line_num
                best_sample_line = line
                best_sample_count = count
        #print(f"best sample found  at line {best_sample_line_num}")
        format = Format(best_sample_line)
        
        
    if format.name == "unknown format":
        print("unknown format")
        return 
    
    args=  ['goaccess', file_path, "-a", #"-o", f"{settings.REPORTS_DIR}/{report_name}",
            "--log-format", f'{format.log_format}',
            f"--date-format={format.date_format}",  
            f"--time-format={format.time_format }"] 
    
    logger(f"trying format {format.name }")
    result =  subprocess.run(
        args,
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
    
