#!/usr/bin/env python
# Copyright 2013 Chase Warwick
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
# run python freetests.py

class HTTP_Parser():

    def __init__(self, HTTP_request):
        self.path = self.initialize_path(HTTP_request)
        self.content_type = self.initialize_content_type(HTTP_request)
        self.request_method = self.initialize_request_method(HTTP_request)

    def initialize_request_method(self, HTTP_request):
        """
        This function returns the method of an HTTP request
        """
        return str(HTTP_request).split('\n')[0].split(' ')[0]

    def initialize_content_type(self, HTTP_request):
        """
        This function returns the http response which indicates the content
        of the current file
        """
        file_types = ['html', 'css']
        for type in file_types:
            if type in self.path:
                return 'Content-Type:text/' + type
        return 'Content-Type:application/octet-stream'
    
    def initialize_path(self, data):
        """
        This function returns the location where the requested file lies
        within the file path
        """
        file_name = './www' + str(data).split('\n')[0].split(' ')[1]

        if file_name[-1] == '/':
            file_name += 'index.html'
        
        return file_name
    
    def get_path(self):
        return self.path
    
    def get_content_type(self):
        return self.content_type

    def get_request_method(self):
        return self.request_method
    
    def construct_HTTP_response(self, status, location=None):
        reponse = None

        if status == 200:
            response = 'HTTP/1.1 200 OK\r\n' + self.content_type + '\r\n' + 'Connection: close\r\n' + '\r\n' + open(self.path, 'r').read() + '\r\n'
        elif status == 301:
            assert not location is None
            response = 'HTTP/1.1 301 Moved Permanently\r\n' + 'Connection: close\r\n' + 'location: /deep/\r\n' + '\r\n'
        elif status == 404:
            response = 'HTTP/1.1 404 Not Found\r\n' + 'Connection: close\r\n' + '\r\n'
        elif status == 405:
            response = 'HTTP/1.1 405 Not Found\r\n' + 'Connection: close\r\n' + '\r\n'

        return response
