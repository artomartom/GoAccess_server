#from flask import Flask, request, abort, jsonify # type: ignore
from fastapi import FastAPI, Request, Query
import uvicorn
import json
import subprocess
#app = Flask(__name__)
app = FastAPI()

from tempfile  import  TemporaryDirectory
from settings import LISTEN,  DEBUG, PORT, VERSION, HOSTNAME
import os
 
from utility import random_string, logger
from fastapi.responses import HTMLResponse
from report_generator import run_goaccess, get_report_url, get_report_file_name
from bench import bench

 
file_dir = "/tmp/ga_tmp/"

error_page= """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>{text} HTML!</h1>
        </body>
    </html>
    """
 
import time
 
@app.get("/v1/report/{file_id}", response_class=HTMLResponse) 
async def get_report(file_id):
    try: 
        
        file_path = os.path.join(file_dir , file_id)
        result = run_goaccess(file_path,"unused")

        return HTMLResponse(content=result.stdout, status_code=200)
       
    except Exception as e:
        return HTMLResponse(content=error_page.format(text = str(e) ), status_code=500)

@app.post("/v1/upload") 
async def get_report( request: Request): 
    try: 
        start = time.time()
        report_filename = get_report_file_name()
        

        logger (f"report file name {report_filename}")
        url = f"{ HOSTNAME}/v1/report/{report_filename}" 

        data =  await request.body()
        
        if len(data) ==  0:
            raise Exception("Empty file")

        logger(f"writing  data")
        with open(f"{file_dir}/{report_filename}", 'w') as f:
            f.write( data.decode("utf-8"))    
 
       
        return  {
            'report': url ,
            'status': 'OK',
            'version': VERSION,
            'time' :  time.time() - start 
        }

    except Exception as e:
        return  {
            'status': 'error',
            'message': str(e),
            'version': VERSION
        }



if __name__ == '__main__':
    uvicorn.run( 
        app="app:app",  # Path to your FastAPI app (module:app)
        port=int(PORT), 
        #reload=True,     # Enable auto-reload for development
        workers=4,       # Number of worker processes (1 for development)
        log_level="info",  # Logging level
        access_log=True,   # Enable access logs
        timeout_keep_alive=5,  
                host=LISTEN)
    #app.run(host=LISTEN, port=int(PORT), debug=DEBUG)