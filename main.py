#!/usr/bin/python3


from http.server import  HTTPServer
from request_handler import  GoAccessRequestHandler 


import os
import shutil
import threading
from time import sleep

from settings import LISTEN
from settings import PORT


reportfolder =  os.path.join(os.getcwd(),'reports')



class WebServer(threading.Thread):
    def __init__(self):
        super().__init__()
        self.host = LISTEN
        self.port = int(PORT)
        self.ws = HTTPServer((self.host, self.port), GoAccessRequestHandler)


    def run(self):
           print("WebServer started at Port:", self.port)
           self.ws.serve_forever()

    def shutdown(self):
            # set the two flags needed to shutdown the HTTP server manually
            self.ws._BaseServer__is_shut_down.set()
            self.ws.__shutdown_request = True

            print('Shutting down server.')
            # call it anyway, for good measure...
            self.ws.shutdown()
            print('Closing server.')
            self.ws.server_close()
            print('Closing thread.')
            self.join()

 

if __name__=='__main__':
    webServer = WebServer()
    webServer.start()
    while True:
        try:
            sleep(1)
        except KeyboardInterrupt:
            print('Keyboard Interrupt sent.')
            webServer.shutdown()
            exit(0)