#  coding: utf-8 
import socketserver
import os

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

        self.data = self.request.recv(1024).strip().decode('utf-8')
        print ("Got a request of: %s\n" % self.data)
        file_location = self.get_file_location(self.data)

        #Handle case where requested file does not exist
        if self.is_404_error(file_location):
            print("Client attempted to access nonexistant path: " + file_location + ":Sending Not Found status code\n")
            self.request.sendall(bytearray('HTTP/1.1 404 Not Found', 'utf-8'))
            return
        #Handle case where requested file is forbidden
        if self.is_405_error(file_location):
            print("Client attempted to access forbidden URL: " + file_location + ":Sending Not Found status code\n")
            self.request.sendall(bytearray('HTTP/1.1 405 Not Found', 'utf-8'))
            return
        
        file_content = self.get_file_content(file_location)
        #Handle general case
        if os.path.isfile(file_location):
            self.request.sendall(bytearray("HTTP/1.1 200 OK",'utf-8'))
            self.request.sendall(bytearray(file_content, 'utf-8'))
            self.request.sendall(bytearray(open(file_location, 'r').read(), 'utf-8'))
        else:
            self.request.sendall(bytearray("HTTP/1.1 200 OK",'utf-8'))

    def get_file_location(self, data):
        """
        This function returns the location where the requested file lies
        within the file path
        """
        FORBIDDEN_URLS = ['deep/']

        file_name = './www' + str(data).split('\n')[0].split(' ')[1]

        for forbidden_url in FORBIDDEN_URLS:
            if forbidden_url in file_name:
                return file_name

        if file_name[-1] == '/':
            file_name += 'index.html'
        
        return file_name

    def get_file_content(self, file_location):
        """
        This function returns the http response which indicates the content
        of the current file
        """
        file_types = ['html', 'css']
        for type in file_types:
            if type in file_location:
                return '\nContent-Type:text/' + type + '\n'
        return '\nContent-Type:text/plain\n'
    
    def is_404_error(self, URL):
        """
        This function checks if a 404 error should be thrown which occurs
        in two cases, the path does not exist or the path given is outside of
        www directory
        """
        FORBIDDEN_URLS = ['../']
        if not os.path.exists(URL):
            return True
        for forbidden_url in FORBIDDEN_URLS:
            if forbidden_url in URL:
                return True
        return False
    
    def is_405_error(self, URL):
        #NEEDS IMPLEMENTATION
        """
        This function returns true if a 405 error should be thrown
        which occurs when the client uses a method which is not permitted
        """
        return False

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
