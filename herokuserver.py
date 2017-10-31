from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
import os

PORT = int(os.environ.get('PORT', 8080))

class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"<html><body>Heroku is awesome</body></html>")

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

try:
    server = ThreadedTCPServer(('', PORT), myHandler)
    print ('Started httpserver on port ' , PORT)
    server.allow_reuse_address = True
    server.serve_forever()

except KeyboardInterrupt:
    print ('CTRL + C RECEIVED - Shutting down the REST server')
    server.socket.close()