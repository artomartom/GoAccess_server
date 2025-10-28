import uuid
import subprocess

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

    if Settings.geoip_db:
        args.extend([ "--geoip-database",Settings.geoip_db ])
    # TODO check if exists Settings.geoip_db and disable 

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


