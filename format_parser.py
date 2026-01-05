

import regex as re
from utility import  Logger as log
import sys


class Fields:
    a_v4 = r"((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}"
    a_v6 = r"([0-9a-fA-F]{1,4}(?::[0-9a-fA-F]{1,4}){7}|::|:(?::[0-9a-fA-F]{1,4}){1,6}|[0-9a-fA-F]{1,4}:(?::[0-9a-fA-F]{1,4}){1,5}|(?:[0-9a-fA-F]{1,4}:){2}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){3}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){4}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){5}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,6}:)"

    mthd = r"(GET|HEAD|PUT|POST|DELETE|PATCH|OPTIONS)"
    url = r"(\/([a-zA-Z0-9\$\-\_\.\+\!\*\'\(\)\\;\/\,\?\:\@\=\&\%]+)?|\*)"
    rfr = r"https?\:\/\/(([0-9a-z\-]+\.){1,8}([a-zA-Z]+|xn--p1ai)|" + a_v4 + "|" + a_v6 + r")(:\d+)?/?" + rf"{url}?" 
    http = r"HTTP\/[0123].[012689]"
    ip = rf"({a_v4}|{a_v6})"
    x_for = rf"{ip}(, {ip})?"
    sts = r"[1-5][0-9][0-9]"
    byt = r"\d+|"
    agnt = r'''(?:(?!\").)*'''
    datim = r"[0-9][0-9]\/[A-Z][a-z][a-z]\/202[0-9]:[0-9][0-9]:[0-9][0-9]:[0-9][0-9]"
    timzn = r"(\+|\-)[0-9][0-9]00"
    upstrm = r"\d+.\d+"
    usr = r"\w+"

    mthd = fr"(?P<mthd>{mthd})"
    url = fr"(?P<url>{url})"
    rfr = fr"(?P<rfr>(\-|{rfr}))"
    http = fr"(?P<http>{http})"
    ip = fr"(?P<ip>{ip})"
    x_for = fr"(?P<x_for>(\-|{x_for}))"
    sts = fr"(?P<sts>{sts})"
    byt = fr"(?P<byt>(\-|{byt}))"
    agnt = fr"(?P<agnt>{agnt})"
    datim = fr"(?P<datim>{datim})"
    timzn = fr"(?P<timzn>{timzn})"
    upstrm = fr"(?P<upstrm>(\-|{upstrm}))"
    usr = fr"(?P<usr>(\-|{usr}))"

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
    "combined_x_for": "%^ %e[%d:%t %^] \"%r\" %s %b \"%R\" \"%u\" \"%h\"",
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

    def __init__(self,_format:tuple=format_list[0]):
        _, self.log_format,self.date_format,self.time_format,self.name = _format
        
    @staticmethod
    def _match_line(sample_line:str):

        for format_type in format_list:
            pattern = re.compile(format_type[0])

            match = pattern.fullmatch(sample_line)

            if match:
                return format_type

        return [None] * 5

    @staticmethod
    def get_format_by_name(log_strings:list[str],name:str,translate:bool=False):
        if name:
            log.debug(f"trying {name} log format")
            for  format_type in format_list:
                if format_type[4] == name :
                    if translate:
                        format_type.log_format = format_translated_real_ip.get(format_type.name,format_type.log_format)
                    return Format(format_type)
            raise Format.Exception(f"unknown format name: {name}")


    @staticmethod
    def get_format(log_strings:list[str],translate:bool ):
        res_format:Format=None
        log.debug("Format with sample_line")
                      
        split:int = 8
        step = int(len(log_strings)/split)
        
        log.debug(f"testing lines:")
        for index in range(split):
            line = log_strings[int(index*step)]
            log.debug(line)
            res_format = Format(Format._match_line(line))
            if res_format.name:
                if translate:
                    res_format.log_format = format_translated_real_ip.get(res_format.name,res_format.log_format)
                return res_format
            
        raise Format.Exception(f"unknown format")
