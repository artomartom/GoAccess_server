

from dotenv import dotenv_values 

config = dotenv_values(".env")   

HOSTNAME =  config["HOSTNAME"]
LISTEN =  config["LISTEN"]  
PORT = config["PORT"]  
VERSION = config["VERSION"]  

CACHE_SRV = None
CACHE_PORT  = None
CACHE = False

if "CACHE" in config:
	CACHE = True
	CACHE_SRV = config["CACHE_SRV"]  
	CACHE_PORT = config["CACHE_PORT"]
   

DEBUG = False
if "DEBUG" in config:
	DEBUG = True

if "HUNTER" in config:
	import hunter
	hunter.trace(module_in=['database','app','cache','report_generator','format_parser'])