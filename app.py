from flask import Flask, request, abort, jsonify

app = Flask(__name__)
from tempfile  import  TemporaryDirectory
from settings import LISTEN,  DEBUG, PORT
import os

from utility import random_string

from report_generator import run_Goaccess, build_url, get_report_file_name


tmp_dir = TemporaryDirectory(  )
@app.route('/generate_report', methods=['POST'])
def get_square():
    try:
        # Get the request data (works with JSON, form data, or raw text)
        data = request.get_data(as_text=True)  # Get raw data as text
        if len(data) ==  0:
            raise Exception( "Empty file")
        log_file_tmp_path = os.path.join(tmp_dir.name, f"{random_string()}.log")
        # Write the data to file
        with open(log_file_tmp_path, 'w') as f:
            f.write(data)
        report_filename = get_report_file_name()
        print (f"report file name {report_filename}")
        result =  run_Goaccess(log_file_tmp_path,report_filename)
        print (f"building url")
        url = build_url(report_filename)
        
        if result.returncode != 0:
            raise Exception( result.stderr)
        
        return jsonify({
            'status': 'OK',
            'report': url
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host=LISTEN, port=int(PORT), debug=DEBUG)
