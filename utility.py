import string
import secrets



class Logger():
    @staticmethod
    def verbose(text):
        print (f"               {text}")

    @staticmethod
    def info(text):
        print (f"               {text}")
    @staticmethod
    def error(text):
        print (f"               {text}")
