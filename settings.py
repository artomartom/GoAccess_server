

from dotenv import dotenv_values 

config = dotenv_values(".env")  # Returns a dict


HOSTNAME =  config["HOSTNAME"]
LISTEN =  config["LISTEN"] #'0.0.0.0'
PORT = config["PORT"] #  3050
VERSION = config["VERSION"] #  3050

DEBUG = False
if "DEBUG" in config:
	DEBUG = True
