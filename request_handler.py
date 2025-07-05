from http.server import BaseHTTPRequestHandler
from tempfile  import  TemporaryDirectory
import os
from http import HTTPStatus
import html
import sys

from report_generator import run_Goaccess
from inspect import currentframe, getframeinfo

import datetime

def get_report_file_name():
    now = datetime.datetime.now()

    formatted_date = now.strftime("%H:%M:%S_%y%m%d_report.html")
    
    return formatted_date

    

#GOACCESS_ERROR_MESSAGE = """ %(code)d %(message)s %(explain)s  """

class GoAccessRequestHandler(BaseHTTPRequestHandler):
   


    tmp_dir = TemporaryDirectory()

    def send_go_access_error(self, code, message=None, explain=None):

        
        self.log_error("code %d, message %s ", code, message )
        print(explain, file=sys.stderr) 
        self.send_response(code, message)
        self.send_header('Connection', 'close')

        content = (""" %(code)d %(message)s %(explain)s  """ % {
            'code': code,
            'message': html.escape(message, quote=False),
            'explain': html.escape(explain, quote=False)
        })
        body = content.encode('UTF-8', 'replace')
        self.send_header("Content-Type", self.error_content_type)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()

        if self.command != 'HEAD' and body:
            self.wfile.write(body)
     
    def do_POST(self):
        # Check if this is a file upload
        if 'content-length' not in self.headers:
            self.send_error(411, "Length Required")
            return
 
        content_length = int(self.headers['content-length'])
        if content_length == 0:
            self.send_error(400, "Empty file")
            return
        # Create a temporary directory to store the uploaded file
        log_file_tmp_path = os.path.join(self.tmp_dir.name, 'access.log')
        body = self.rfile.read(content_length)

        with open(log_file_tmp_path, 'wb') as f:
            f.write(body)

        
        result =  run_Goaccess(log_file_tmp_path,get_report_file_name())

        if result.returncode != 0:
            
            self.send_go_access_error(HTTPStatus.BAD_REQUEST, "error", result.stderr )
             
            return

        self.send_header('Content-type', 'text/plain') 
        self.send_response(200,"ok")
        self.end_headers()
      