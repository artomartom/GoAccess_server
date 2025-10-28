import string
import secrets

from settings import  Settings


class Logger():
    @staticmethod
    def verbose(text:str):
        if  Settings.loglevel == 'verbose' :
            print (f"               {text}")

    @staticmethod
    def info(text:str):
        if Settings.loglevel in ['info','verbose','warn']:
            print (f"               {text}")
    @staticmethod
    def warn(text:str):
        if Settings.loglevel in ['info','verbose','warn']:
            print (f"               {text}")
    @staticmethod
    def error(text:str):
        print (f"               {text}")
