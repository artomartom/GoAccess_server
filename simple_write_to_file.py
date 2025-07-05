#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from datetime import datetime

PORT = 3050
OUTPUT_DIR = "received_data"  # Directory where files will be saved

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Read the request body
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        
        # Create output directory if it doesn't exist
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
        
        # Generate a filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"{OUTPUT_DIR}/received_{timestamp}.data"
        
        # Write the body to file
        with open(filename, 'wb') as f:
            f.write(body)
        
        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(f"Data saved to {filename}".encode())
    
    def do_GET(self):
        # Optional: Handle GET requests if needed
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Server is running. Send POST requests to store data.")

def run_server():
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f"Server running on port {PORT}")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
