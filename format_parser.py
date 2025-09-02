

import re
from utility import  logger
"""
[0] regex
[1] log format
[2] date format
[3] time format
[4] name
"""

class Fields:
    a_v4 = r"((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}"
    a_v6 = r"([0-9a-fA-F]{1,4}(?::[0-9a-fA-F]{1,4}){7}|::|:(?::[0-9a-fA-F]{1,4}){1,6}|[0-9a-fA-F]{1,4}:(?::[0-9a-fA-F]{1,4}){1,5}|(?:[0-9a-fA-F]{1,4}:){2}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){3}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){4}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){5}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,6}:)"
    mthd = r"(GET|HEAD|PUT|POST|DELETE|PATCH)"
    url = r"\/([a-zA-Z0-9\$\-\_\.\+\!\*\'\(\)\\;\/\,\?\:\@\=\&\%]+)?"
    rfr = r"(?:http[s]?:\/\/.)((?:www\.)?[-a-zA-Z0-9@%._\+~#=]{2,256}\.[a-z]{2,6}\b(?:[-a-zA-Z0-9@:%_\+.~#?&\/\/=]*)(|:\d)|((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}|([0-9a-fA-F]{1,4}(?::[0-9a-fA-F]{1,4}){7}|::|:(?::[0-9a-fA-F]{1,4}){1,6}|[0-9a-fA-F]{1,4}:(?::[0-9a-fA-F]{1,4}){1,5}|(?:[0-9a-fA-F]{1,4}:){2}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){3}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){4}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){5}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,6}:))(:(\d+\/?))?" + fr"({url})?"
    http = r"HTTP\/[0123].[012689]"
    ip = rf"({a_v4}|{a_v6})"
    x_for = rf"{ip}(, {ip})?"
    sts = r"[1-5][0-9][0-9]"
    byt = r"\d+"
    agnt = r'''(?:(?!\").)*'''
    datim = r"[0-9][0-9]\/[A-Z][a-z][a-z]\/202[0-9]:[0-9][0-9]:[0-9][0-9]:[0-9][0-9]"
    timzn = r"(\+|\-)0[0-9]00"
    upstrm = r"(\d+.\d+|\-)"
    usr = r"(-|\w+)"
    combined = fr'''({a_v4}|{a_v6}) - {usr} \[{datim} {timzn}\] \"{mthd} {url} {http}\" {sts} {byt} \"({rfr}|-)\" \"{agnt}\"'''
    bitrixvm_main = fr'''({ip}|{ip}) - {usr} \[{datim} {timzn} - ({upstrm}|-)\] {sts} \"{mthd} {url} {http}\" {byt} \"({rfr}|-)\" \"{agnt}\" \"({x_for}|-)\"'''
    combined_x_for = fr'''({a_v4}|{a_v6}) - {usr} \[{datim} {timzn}\] \"{mthd} {url} {http}\" {sts} {byt} \"({rfr}|-)\" \"{agnt}\" \"({x_for}|-)\"'''
    hestia = fr'''({a_v4}|{a_v6}) - {usr} \[{datim} {timzn}\] {mthd} {url} {http} \"{sts}\" {byt} \"({rfr}|-)\" \"{agnt}\" \"({x_for}|-)\"'''
    litespeed = fr'''\"({a_v4}|{a_v6}) - {usr} \[{datim} {timzn}\] \"{mthd} {url} {http}\" {sts} {byt} \"({rfr}|-)\" \"{agnt}\"\"'''
 
format_list =  [
    (Fields.combined, 
    "%h %e[%d:%t %^] \"%r\" %s %b \"%R\" \"%u\"",  "%d/%b/%Y",  "%T" , "combined" ),
    (Fields.bitrixvm_main,
    "%h - %e [%d:%t - %T] %s \"%r\" %b \"%R\" \"%u\" \"%^\"","%d/%b/%Y",'%H:%M:%S',"bitrixvm_main"),
    (Fields.combined_x_for,
    "%h %e[%d:%t %^] \"%r\" %s %b \"%R\" \"%u\"  \"%^\"","%d/%b/%Y",'%H:%M:%S',"combined_x_for"),
    (Fields.hestia,
    "%h - %e [%d:%t - %^] %m %U %H \"%s\" %b \"%R\" \"%u\" \"%^\"","%d/%b/%Y",'%H:%M:%S',"hestia"),
    (Fields.litespeed,
    "\"%h %e[%d:%t %^] \"%r\" %s %b \"%R\" \"%u\"\"",  "%d/%b/%Y",  "%T" , "litespeed" ),
    ]

class Format():
    
    class  Exception(Exception):
            pass 
    
    def __init__(self,sample_line=None,name="combined"):
        if sample_line:
            logger("Format with sample_line")
            _, self.log_format,self.date_format,self.time_format,self.name = Format.match_line(sample_line)
            return 
        if name:
            logger("Format with name")
            for format in format_list:
                if format[4] == name :
                    _, self.log_format,self.date_format,self.time_format,self.name = format
                    return 
            raise Format.Exception(f"unknown format name: {name}")
        
    def match_line(sample_line):
        
        for format in format_list:
            pattern = re.compile(format[0])
            
            match = pattern.fullmatch(sample_line)
            
            if match:
                return format
               
        raise Format.Exception(f"unknown format line: {sample_line}")
    
    def get_format(log_strings : list[str],name :str ):
        
        if name != "":
            logger (f"trying {name} log format")
            return Format(name=name)

        logger ("trying to deduce log format")
        best_sample_line: str = ""
        best_sample_line_num: int = 0
        count = len(log_strings) 
        best_sample_count: int  = 500
        for line_num in range(count):    
            line = log_strings[line_num]
            count = line.count('"-"')
            if best_sample_count > count:
                best_sample_line_num = line_num
                best_sample_line = line
                best_sample_count = count
        logger(f"best sample line {best_sample_line}")
        return  Format(sample_line=best_sample_line)
