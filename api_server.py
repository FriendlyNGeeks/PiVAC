# START WEB SERVER
#####################################################################
# Python 3 server example
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json

server_address = ('0.0.0.0', 80)

class MyServer(BaseHTTPRequestHandler):
    
    def do_GET(self):
        jData = json.loads(os.environ.get('jsonData').replace("\'", "\""))
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        test = str(jData)
        self.wfile.write(bytes(test.replace("\'", "\""), "utf-8"))
        # self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        # self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        # self.wfile.write(bytes("<body>", "utf-8"))
        # self.wfile.write(bytes("<p>"+jsonString+"</p>", "utf-8"))
        # self.wfile.write(bytes("</body></html>", "utf-8"))

class apiHttp():
    def __init__(self):
        self.dt = datetime.now()
        self.ts = datetime.timestamp(self.dt)
        self.date_time = datetime.fromtimestamp(self.ts)
        self.utc_ts = self.date_time.strftime("%d-%m-%Y, %H:%M:%S")
        self.webServer = HTTPServer(server_address, MyServer)
        
    def start(self):
        print("Server starting http://%s:%s" % server_address, "@", self.utc_ts)
        try:
            print("it started for real")
            self.webServer.serve_forever()
        except KeyboardInterrupt:
            pass

        self.webServer.server_close()
        print("Server stopped.")
#####################################################################
# END WEB SERVER
