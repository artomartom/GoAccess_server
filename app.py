from flask import Flask, request, abort, jsonify # type: ignore

app = Flask(__name__)
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
            f.write(data)
            
def write_regex(path,data,regex):
    logger(f"parsing regex{regex}")
    with open(path, 'w') as f:
        for line in data.split('\n'):
            if re.search(regex, line):
                f.writelines(line)  

@app.route('/v1/report', methods=['POST'])
def get_report():
    try:
        # Get the request data (works with JSON, form data, or raw text)
        log_file_tmp_path = os.path.join(tmp_dir.name, f"{random_string()}.log")
        
        match = request.args.get('mth')
        
        logger(f"found match argument: {match}")

        data = request.get_data(as_text=True)  # Get raw data as text
        if len(data) ==  0: 
            raise Exception( "Empty file")

        start = time.time()
        if match == None:
            write_raw(log_file_tmp_path, data)
        else:
            write_regex(log_file_tmp_path, data, match) 
        end = time.time()
        
        logger(f"writing time {end - start}")
            
        report_filename = get_report_file_name()
        logger (f"report file name {report_filename}")
        result =  run_Goaccess(log_file_tmp_path,report_filename)
        url = build_url(report_filename)
        
        if result.returncode != 0:
            raise Exception( result.stderr)
        
        return jsonify({
            'report': url ,
            'status': 'OK',
            'version': VERSION
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'version': VERSION
        }), 500

if __name__ == '__main__':
    app.run(host=LISTEN, port=int(PORT), debug=DEBUG)
