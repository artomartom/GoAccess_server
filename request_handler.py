from http.server import BaseHTTPRequestHandler
from tempfile  import  TemporaryDirectory
import os
from http import HTTPStatus
import html
import sys

from report_generator import run_Goaccess, build_url
from inspect import currentframe, getframeinfo

import datetime
import hashlib

import   settings  

def get_report_file_name():
     
    #formatted_date =  datetime.datetime.now().strftime("%H:%M:%S_%y%m%d") 
    formatted_date =  datetime.datetime.now().strftime("%H%M%S%f%Y") 
    hash =  hashlib.sha256(formatted_date.encode()).hexdigest() 
  
    return   f"access_report_{str(hash[:20])}.html"


import secrets
import string

def random_string(length=12):
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))



class GoAccessRequestHandler(BaseHTTPRequestHandler):

    tmp_dir = TemporaryDirectory(delete=False )

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
        log_file_tmp_path = os.path.join(self.tmp_dir.name, f"{random_string()}.log")
        body = self.rfile.read(content_length)

        with open(log_file_tmp_path, 'wb') as f:
            f.write(body)

        report_filename = get_report_file_name()
        print (f"report file name {report_filename}")
        result =  run_Goaccess(log_file_tmp_path,report_filename)
        
        if result.returncode != 0:
            
            self.send_go_access_error(HTTPStatus.BAD_REQUEST, "error", result.stderr )
             
            return

        print (f"building url")
        url = build_url(report_filename)


        #self.send_header('Content-type', 'text/html')  
        ##self.protocol_version
        #self.send_response(200,"ok")
        #self.end_headers()
        self.protocol_version = 'HTTP/1.1'
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length",len(url.encode('utf-8')) )
        self.end_headers()
        self.wfile.write(bytes(url, "utf-8"))
      