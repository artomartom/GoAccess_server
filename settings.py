

from dotenv import dotenv_values 

config = dotenv_values(".env")   

HOSTNAME =  config["HOSTNAME"]
LISTEN =  config["LISTEN"]  
PORT = config["PORT"]  
VERSION = config["VERSION"]  

if "CACHE" in config:
	CACHE_SRV = config["CACHE_SRV"]  
	CACHE_PORT = config["CACHE_PORT"]  

DEBUG = False
if "DEBUG" in config:
	DEBUG = True
