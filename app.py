#from flask import Flask, request, abort, jsonify # type: ignore
from fastapi import FastAPI, Request
import uvicorn
import json

#app = Flask(__name__)
app = FastAPI()

from tempfile  import  TemporaryDirectory
from settings import LISTEN,  DEBUG, PORT, VERSION
import os

from utility import random_string, logger

from report_generator import run_Goaccess, build_url, get_report_file_name
from bench import bench

tmp_dir = TemporaryDirectory(  )

@app.route('/v1/bench', methods=['POST'])
def get_bench():
    res = bench(request.get_data(as_text=True))
    print(res)
    return jsonify({
            'status': 'OK',
            'time': res
        }), 200

import time
import re

def write_raw(path,data):
    logger(f"writing raw data")
    with open(path, 'w') as f:
            f.write( data.decode("utf-8"))

def write_regex(path,data,regex):
    logger(f"parsing regex{regex}")
    with open(path, 'wb') as f:
        for line in data.decode("utf-8").split('\n'):
            if re.search(regex, line):
                f.writelines(line)

 

@app.post("/v1/report")
async def get_report(request: Request):
    try:
        start = time.time()
        # Get the request data (works with JSON, form data, or raw text)
        log_file_tmp_path = os.path.join(tmp_dir.name, f"{random_string()}.log")

        match = request.query_params['mth']
        logger(f"found match argument: {match}")
        #logger(f"found arguments: {request.args}")

        report_filename = get_report_file_name()
        logger (f"report file name {report_filename}")
        url = build_url(report_filename)
        

        logger(f"sync point")
        data =  await request.body()
        
        if len(data) ==  0:
            raise Exception("Empty file")
        if match == None:
            write_raw(log_file_tmp_path, data)
        else:
            write_regex(log_file_tmp_path, data, match)


        result =  run_Goaccess(log_file_tmp_path,report_filename)

        if result.returncode != 0:
            raise Exception( result.stderr)

        return  {
            'report': url ,
            'status': 'OK',
            'version': VERSION,
            'time' :  time.time() -start
            
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