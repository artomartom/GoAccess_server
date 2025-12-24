

import regex as re
from utility import  Logger as log
import sys


class Fields:
    a_v4 = r"((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}"
    a_v6 = r"([0-9a-fA-F]{1,4}(?::[0-9a-fA-F]{1,4}){7}|::|:(?::[0-9a-fA-F]{1,4}){1,6}|[0-9a-fA-F]{1,4}:(?::[0-9a-fA-F]{1,4}){1,5}|(?:[0-9a-fA-F]{1,4}:){2}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){3}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){4}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){5}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,6}:)"

    mthd = r"(GET|HEAD|PUT|POST|DELETE|PATCH|OPTIONS)"
    url = r"(\/([a-zA-Z0-9\$\-\_\.\+\!\*\'\(\)\\;\/\,\?\:\@\=\&\%]+)?|\*)"
    rfr = r"((?:http[s]?:\/\/.)((?:www\.)?[-a-zA-Z0-9@%._\+~#=]{2,256}\.[a-z]{2,6}\b(?:[-a-zA-Z0-9@:%_\+.~#?&\/\/=]*)(|:\d)|((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}|" + a_v6 + r")(:(\d+\/?))?" + fr"({url})?|-)"
    http = r"HTTP\/[0123].[012689]"
    ip = rf"({a_v4}|{a_v6})"
    x_for = rf"(-|{ip}(, {ip})?)"
    sts = r"[1-5][0-9][0-9]"
    byt = r"(\d+|-)"
    agnt = r'''(?:(?!\").)*'''
    datim = r"[0-9][0-9]\/[A-Z][a-z][a-z]\/202[0-9]:[0-9][0-9]:[0-9][0-9]:[0-9][0-9]"
    timzn = r"(\+|\-)0[0-9]00"
    upstrm = r"(\d+.\d+|\-)"
    usr = r"(-|\w+)"

    mthd = fr"(?P<mthd>{mthd})"
    url = fr"(?P<url>{url})"
    rfr = fr"(?P<rfr>{rfr})"
    http = fr"(?P<http>{http})"
    ip = fr"(?P<ip>{ip})"
    x_for = fr"(?P<x_for>{x_for})"
    sts = fr"(?P<sts>{sts})"
    byt = fr"(?P<byt>{byt})"
    agnt = fr"(?P<agnt>{agnt})"
    datim = fr"(?P<datim>{datim})"
    timzn = fr"(?P<timzn>{timzn})"
    upstrm = fr"(?P<upstrm>{upstrm})"
    usr = fr"(?P<usr>{usr})"

    combined = fr'''{ip} - {usr} \[{datim} {timzn}\] \"{mthd} {url} {http}\" {sts} {byt} \"{rfr}\" \"{agnt}\"\n?'''
    bitrixvm_main = fr'''{ip} - {usr} \[{datim} {timzn} - {upstrm}\] {sts} \"{mthd} {url} {http}\" {byt} \"{rfr}\" \"{agnt}\" \"{x_for}\"\n?'''
    combined_x_for = fr'''{ip} - {usr} \[{datim} {timzn}\] \"{mthd} {url} {http}\" {sts} {byt} \"{rfr}\" \"{agnt}\" \"{x_for}\"\n?'''
    hestia = fr'''{ip} - {usr} \[{datim} {timzn}\] {mthd} {url} {http} \"{sts}\" {byt} \"{rfr}\" \"{agnt}\" \"{x_for}\"\n?'''
    litespeed = fr'''\"{ip} - {usr} \[{datim} {timzn}\] \"{mthd} {url} {http}\" {sts} {byt} \"{rfr}\" \"{agnt}\"\"\n?'''

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

format_translated_real_ip = {
    "bitrixvm_main": "%^ - %e [%d:%t - %T] %s \"%r\" %b \"%R\" \"%u\" \"%h\"",
    "combined_x_for": "%^ %e[%d:%t %^] \"%r\" %s %b \"%R\" \"%u\"  \"%h\"",
    "hestia": "%^ - %e [%d:%t - %^] %m %U %H \"%s\" %b \"%R\" \"%u\" \"%h\"",
}

class Format():
    """
    [0] regex
    [1] log format
    [2] date format
    [3] time format
    [4] name
    """

    class  Exception(Exception):
        pass

    def __init__(self,sample_line:str=None,name:str="combined"):
        if sample_line:
            log.debug("Format with sample_line")
            _, self.log_format,self.date_format,self.time_format,self.name = Format.match_line(sample_line)
            return
        if name:
            log.debug("Format with name")
            for  format_type in format_list:
                if format_type[4] == name :
                    _, self.log_format,self.date_format,self.time_format,self.name = format_type
                    return
            raise Format.Exception(f"unknown format name: {name}")
    @staticmethod
    def match_line(sample_line:str):

        for format_type in format_list:
            pattern = re.compile(format_type[0])

            match = pattern.fullmatch(sample_line)

            if match:
                return format_type

        raise Format.Exception(f"unknown format line: {sample_line}")

    @staticmethod
    def get_format(log_strings:list[str],args:dict ):
        name = args['fmt']
        res_format:Format=None
        if name:
            log.debug(f"trying {name} log format")
            res_format = Format(name=name)
        else:
            log.debug("trying to deduce log format")
            best_sample_line: str = ""
            best_sample_line_num: int = 0
            count = len(log_strings)
            best_sample_count: int  = sys.maxsize
            for line_num in range(count):
                line = log_strings[line_num]
                count = line.count('"-"')
                if best_sample_count > count:
                    best_sample_line_num = line_num
                    best_sample_line = line
                    best_sample_count = count
            log.debug(f"best sample line {best_sample_line_num+1} {best_sample_line}")
            res_format =   Format(sample_line=best_sample_line)
        
        if args['trnslt']:
            res_format.log_format = format_translated_real_ip.get(res_format.name,res_format.log_format)
        
        return res_format
