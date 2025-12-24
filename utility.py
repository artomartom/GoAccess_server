
from settings import  Settings

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
