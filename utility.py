
from settings import  Settings
import logging

block_endpoints = ["/health"]

class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if record.args and len(record.args) >= 3:
            path = record.args[2]
            if path in block_endpoints:
                return False
        return True

uvicorn_logger = logging.getLogger("uvicorn.access")
uvicorn_logger.addFilter(EndpointFilter())

#TODO  def debug(**args):
class Logger():
    @staticmethod
    def debug(text:str):
        if  Settings.loglevel == 'debug' :
            print (f"               {text}")

    @staticmethod
    def info(text:str):
        if Settings.loglevel in ['info','debug','warn']:
            print (f"               {text}")
    @staticmethod
    def warn(text:str):
        if Settings.loglevel in ['info','debug','warn']:
            print (f"               {text}")
    @staticmethod
    def error(text:str):
        print (f"               {text}")
