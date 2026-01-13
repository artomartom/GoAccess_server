
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

class Logger():
    @staticmethod
    def debug(*args:str):
        if  Settings.loglevel == 'debug' :
            print (f"               {args}")

    @staticmethod
    def info(*args:str):
        if Settings.loglevel in ['info','debug','warn']:
            print (f"               {args}")
    @staticmethod
    def warn(*args:str):
        if Settings.loglevel in ['info','debug','warn']:
            print (f"               {args}")
    @staticmethod
    def error(*args:str):
        print (f"               {args}")
