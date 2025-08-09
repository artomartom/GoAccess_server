

import re
from utility import  logger
"""
[0] regex
[1] log format
[2] date format
[3] time format
[4] name
"""

format_list =  [
    ( r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4} - (-|\w+) \[[0-9][0-9]\/[A-Z][a-z][a-z]\/202[0-9]:[0-9][0-9]:[0-9][0-9]:[0-9][0-9] \+0[0-9]00] \"(GET|HEAD|PUT|POST|DELETE|PATCH) \/.* HTTP\/[0123].[012689]\" [1-5][0-9][0-9] \d+ \"http(s|):\/\/.*\/*\"" , 
    "%h %^[%d:%t %^] \"%r\" %s %b \"%R\" \"%u\"  %^",  "%d/%b/%Y",  "%T" , "combined" ),
    (r"((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4} - (-|\w+) \[[0-9][0-9]\/[A-Z][a-z][a-z]\/202[0-9]:[0-9][0-9]:[0-9][0-9]:[0-9][0-9] \+0[0-9]00 - (\d+.\d+|\-)] [1-5][0-9][0-9] \"(GET|HEAD|PUT|POST|DELETE|PATCH) \/.* HTTP\/[0123].[012689]\" \d+ \"(http(s|)://.*\/*|\-)\" \"(.*(ozilla|indows|pple|pera|acebook|oogle|bot|BOT|Gecko|rawler|hrome|irefox).*)\" \"(((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}|\-|((([0-9A-Fa-f]{1,4}:){1,6}:)|(([0-9A-Fa-f]{1,4}:){7}))([0-9A-Fa-f]{1,4}))\"",
    "%h - %^ [%d:%t - %^] %s \"%r\" %b \"%R\" \"%u\" %^","%d/%b/%Y",'%H:%M:%S',"bitrixvm main")
    ]


class Format():
    
    
    def __init__(self,sample_line):
        format = Format.match_line(sample_line)
        self.log_format = format[1]
        self.date_format = format[2]
        self.time_format = format[3]
        self.name = format[4] 
    
    def match_line(  sample_line):
        
        for format in format_list:
            pattern = re.compile(format[0])
            
            match = pattern.search(sample_line)
            
            if match:
                return format
            
               
        return  ("unknown format","","","","unknown format")
    

    def get_format(log_strings : str):

        best_sample_line: str = ""
        best_sample_line_num: int = 0
        best_sample_count: int  = 50
        for line_num in range(len(log_strings)):    
            line = log_strings[line_num]
            count = line.count('"-"')
            if best_sample_count > count:
                best_sample_line_num = line_num
                best_sample_line = line
                best_sample_count = count
        logger(f"best sample line {best_sample_line}")
        return  Format(best_sample_line)


if __name__ == "__main__":
    format = Format()
    line = ('78.178.85.171 - - [02/Jul/2025:00:02:25 +0300] "GET /image/catalog/import/peregorodki-i-steny-iz-sehndvich-panelej-30me-2588.webp HTTP/1.1" 200 512156 "https://ryazan.mpaneli.ru/" "Mozilla/5.0 (Linux; arm_64; Android 12; NCO-LX1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.1823 YaApp_Android/24.120.1 YaSearchBrowser/24.120.1 BroPP/1.0 SA/3 Mobile Safari/537.36"')
    print(Format.match_line(line))
