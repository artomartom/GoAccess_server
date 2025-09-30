import string
import secrets

from settings import  LOGLEVEL


class Logger():
    @staticmethod
    def verbose(text):
        if  LOGLEVEL == 'verbose' :
            print (f"               {text}")
            
    @staticmethod
    def info(text):
        if LOGLEVEL in ['info','verbose']:
            print (f"               {text}")
    @staticmethod
    def error(text):
        print (f"               {text}")
