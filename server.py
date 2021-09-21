#  coding: utf-8 
import socketserver
import os

from HTTP_Parser import HTTP_Parser

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
    #FIND BETTER WAY TO HANDLE FORBIDDEN STUFF
    def handle(self):
        """Handles requests from client"""

        data = self.request.recv(1024).strip().decode('utf-8')
        print ("Got a request of: %s\n" % data)
        self.HTTP_parser = HTTP_Parser(data)
        
        if self.should_redirect():
            print("Client should be redirected to a new directory: " + self.HTTP_parser.get_path() + " :Sending 301 status code\n")
            response = self.HTTP_parser.construct_HTTP_response(301)
            self.request.sendall(bytearray(response,'utf-8'))
        if self.is_405_error():
            print("Client made an invalid request: " + self.HTTP_parser.get_request_method() + ":Sending 405 status code\n")
            response = self.HTTP_parser.construct_HTTP_response(405)
            self.request.sendall(bytearray(response, 'utf-8'))
            return
        if self.is_404_error():
            print("Client attempted to access nonexistant path: " + self.HTTP_parser.get_path() + ":Sending 404 status code\n")
            response = self.HTTP_parser.construct_HTTP_response(404)
            self.request.sendall(bytearray(response, 'utf-8'))
            return
        
        response = self.HTTP_parser.construct_HTTP_response(200)
        self.request.sendall(bytearray(response,'utf-8'))

    def should_redirect(self):
        #SHOULD REFACTOR TO ENSURE LESS HARDCODED DATA
        """
        This function checks against a variety of predefined URLs to see if there is a match
        in the case that there is it returns True
        """
        path = self.HTTP_parser.get_path()
        REDIRECT_PATHS = ["./www/deep"]
        for redirect_path in REDIRECT_PATHS:
            if redirect_path == path:
                return True
        return False

    def is_404_error(self):
        """
        This function checks if a 404 error should be thrown which occurs
        in two cases, the path does not exist or the path given is outside of
        www directory
        """
        FORBIDDEN_PATHS = ['../']
        path = self.HTTP_parser.get_path()

        if not os.path.exists(path):
            return True

        for forbidden_path in FORBIDDEN_PATHS:
            if forbidden_path in path:
                return True
        
        return False
    
    def is_405_error(self):
        """
        This function returns true if a 405 error should be thrown
        which occurs when the client uses a method which is not permitted
        """
        method = self.HTTP_parser.get_request_method()

        if not method == 'GET':
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
