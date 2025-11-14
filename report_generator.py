import uuid
import subprocess
import os.path

from settings import  Settings
from  format_parser import Format
from utility import Logger as log

def get_report_url(filename:str):
    return f"{ Settings.external_url}/{filename}"

def new_report_id():
    return  uuid.uuid4().hex

def run_goaccess( filename:str, format_t:Format ) -> str:

    log.verbose(f"trying format {format_t.name }")
    args=  ["goaccess",filename,    "-a",
            "--log-format", f'{format_t.log_format}',
            f"--date-format={format_t.date_format}",
            f"--time-format={format_t.time_format }"]

    if Settings.geoip_db and os.path.isfile(Settings.geoip_db):
        args.extend([ "--geoip-database",Settings.geoip_db ])
    else:
        log.warn(f"Cant find mmdb file {Settings.geoip_db}. Option geoip_db disabled")

    threshold:int = 314572800

    if os.path.getsize(filename) > threshold: # if log file is bigger then 300 mebibyte spawn multiple jobs 
        args.extend([ "--jobs",str(Settings.jobs) ])
    else:
        args.extend([ "--jobs", str(1) ])
        
    result = subprocess.run(
        args,
        capture_output=True,
        check=False
    )

    if result.returncode != 0:
        err = result.stderr.decode()
        log.error(err)
        raise Format.Exception('')
    return result.stdout


