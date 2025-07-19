

from dotenv import dotenv_values 

config = dotenv_values(".env")  # Returns a dict


REPORTS_DIR = config["REPORTS_DIR"] # f"{getcwd()}/reports/"
HOSTNAME =  config["HOSTNAME"]
LISTEN =  config["LISTEN"] #'0.0.0.0'
PORT = config["PORT"] #  3050
DEBUG = config["DEBUG"]
