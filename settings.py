

from  argparse import ArgumentParser,ArgumentDefaultsHelpFormatter
import os.path

def parse_args():
    """Parse command line arguments using argparse"""

    parser = ArgumentParser(
        description='Application configuration parameters',
        formatter_class= ArgumentDefaultsHelpFormatter
    )

    parser.add_argument( '--external-url', type=str, default='http://localhost',help='External URL for the application')

    parser.add_argument( '-l','--listen', type=str, default='0.0.0.0',help='IP address to listen on')

    parser.add_argument( '-p','--port', type=int, default=3050,help='Port to listen on')

    parser.add_argument( '-w', '--worker', type=int, default=4,help='Number of worker processes')

    parser.add_argument( '-j', '--jobs', type=int, default=4,help='Goaccess job count')

    parser.add_argument( '--loglevel', type=str, default='warn',choices=['debug', 'info', 'warn', 'verbose'],
        help='Logging level')

    parser.add_argument( '--geoip-db', type=str, default=None,help='Path to GeoIP database file')

    parser.add_argument( '--cache', action='store_true', help='Enable or disable caching')

    parser.add_argument( '--cache-srv', type=str, default='redis',help='Cache server type' )

    parser.add_argument( '--cache-port', type=int, default=6379,help='Cache server port' )

    parser.add_argument( '--debug', action='store_true', help='Enable or disable debug mode')

    parser.add_argument( '--hunter', action='store_true', help='Enable or disable hunter mode')
    

    return parser.parse_args()

Settings = parse_args()

def check_settings():
    if Settings.geoip_db and not os.path.isfile(Settings.geoip_db):
        raise FileNotFoundError(f"mmdb file {Settings.geoip_db} not found")
    
check_settings()