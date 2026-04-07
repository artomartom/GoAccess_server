from  argparse import ArgumentParser,ArgumentDefaultsHelpFormatter
import os.path
import yaml
from yaml import Loader
from pydantic import BaseModel
from typing import Optional

class Model(BaseModel):
    external_url: Optional[str] = 'http://localhost'
    listen: Optional[str] = '127.0.0.1'
    port: Optional[int] = 3050
    worker: Optional[int] = 1
    jobs: Optional[int] = 1
    geoip_db: Optional[str] = None
    loglevel: Optional[str] = 'warning'
    cache_server: Optional[str] = None
    debug: Optional[bool] = False

class FileSettings:

    model:Model = None

    def __init__(self):
        if os.path.isfile('/etc/goaccess/config.yaml'):
            with open("/etc/goaccess/config.yaml", "r") as f:
                config = yaml.load(f,Loader=Loader)
                self.model = Model(**config)
        else: 
            self.model = Model()

def check_settings():
    if Settings.geoip_db and not os.path.isfile(Settings.geoip_db):
        raise FileNotFoundError(f"mmdb file {Settings.geoip_db} not found")

def parse_args():

    parser = ArgumentParser(
        description='Application configuration parameters',
        formatter_class= ArgumentDefaultsHelpFormatter
    )
    fromfile = FileSettings().model

    parser.add_argument( '--external-url', type=str, default=fromfile.external_url,help='External URL for the application')

    parser.add_argument( '-l','--listen', type=str, default=fromfile.listen,help='IP address to listen on')

    parser.add_argument( '-p','--port', type=int, default=fromfile.port,help='Port to listen on')

    parser.add_argument( '-w', '--worker', type=int, default=fromfile.worker,help='Number of worker processes')

    parser.add_argument( '-j', '--jobs', type=int, default=fromfile.jobs,help='Goaccess job count')

    parser.add_argument( '--loglevel', type=str, default=fromfile.loglevel,choices=['debug', 'info', 'warning'],
        help='Logging level')

    parser.add_argument( '--geoip-db', type=str, default=fromfile.geoip_db,help='Path to GeoIP database file')

    parser.add_argument( '--cache-server', type=str, default=fromfile.cache_server,help='Cache server type' )

    parser.add_argument( '--debug', action='store_true',default=fromfile.debug, help='Enable or disable debug mode')

    return parser.parse_args()

Settings = parse_args()

check_settings()