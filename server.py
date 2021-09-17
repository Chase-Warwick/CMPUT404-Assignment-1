#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        

        self.data = self.request.recv(1024).strip().decode('utf-8')
        print ("Got a request of: %s\n" % self.data)
        URL = self.get_url(self.data)
        print(URL)

        if self.is_forbidden(URL):
            print("Client attempted to access forbidden URL:Sending forbidden status code")
            self.request.sendall(bytearray('HTTP/1.1 403 Forbidden', 'utf-8'))
            return
                
        self.request.sendall(bytearray("HTTP/1.1 200 OK",'utf-8'))
        if "GET / HTTP/1.1" in str(self.data):
            self.request.sendall(bytearray(open("./www/index.html", 'r').read(), 'utf-8'))
        if "base.css" in str(self.data):
            self.request.sendall(bytearray(open("./www/base.css", 'r').read(), 'utf-8'))
    
    def get_url(self, data):
        #REWRITE THIS
        """
        This function returns the first line of the request from the client which
        includes the URL
        """
        return str(data).split('\n')[0].split(' ')[1]
    
    def is_forbidden(self, URL):
        """
        This function returns true if it finds that the URL
        is within a forbidden subdirectory
        """
        FORBIDDEN_URLS = ["/deep/"]

        for forbidden_URL in FORBIDDEN_URLS:
            if forbidden_URL in URL:
                return True
        return False
            

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
