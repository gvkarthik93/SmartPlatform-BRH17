#! /usr/bin/env python3

import http.server
from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
from os import curdir, sep, environ
import mimetypes
import cgi
import threading
import sqlite3
import json

#PORT = 8126
PORT = environ['PORT']

#This class will handle any incoming request from the browser
class myHandler(BaseHTTPRequestHandler):
    #Handler for GET requests
    def do_GET(self):
        if self.path=="/":
            self.path="/index.html"

        if self.path=="/index":
            self.path="/index.html"

        try:
            #Open the static file requested and send it
            #Check the file extension required
            #Set the right mime type
            #rb is used to read all the mime types and display them
            f = open(curdir + sep + self.path, 'rb')
            mimetype, _ = mimetypes.guess_type(self.path)
            try:
                self.send_response(200)
                self.send_header('Content-type',mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            except:
                print ("Connection Aborted: Established connection has been dropped")
            return
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

    #Handler for POST requests
    #do_POST function gets execcuted for every POST request from client
    def do_POST(self):
        try:
            if self.path == "/searchDetails":
                try:
                    print (searchDetail)
                    #self.wfile.write(searchDetail.encode("utf-8"))
                except:
                    print ("Unable to fetch search detail")

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

#Each time a request comes in, a new thread or process is created to handle it
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass
#Swapping ForkingMixIn for ThreadingMixIn above would achieve similar results, using separate process instead of threads

try:
    #Create a web server and define the handler to manage the
    #incoming request
    #server = HTTPServer(('', PORT), myHandler)
    server = ThreadedTCPServer(('', PORT), myHandler)
    print ('Started httpserver on port ' , PORT)
    
    ip,port = server.server_address

    #Start a thread with the server - that thread will then start one more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    #Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    allow_reuse_address = True

    #Wait forever for incoming http requests
    server.serve_forever()

except KeyboardInterrupt:
    print ('CTRL + C RECEIVED - Shutting down the web server')
    server.socket.close()