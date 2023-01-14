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
        if os.environ.get('jsonData') != "null":
            jData = json.loads(os.environ.get('jsonData').replace("\'", "\""))
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            payload = str(jData)
            self.wfile.write(bytes(payload.replace("\'", "\""), "utf-8"))
        else:
            self.send_response(200)
            self.wfile.write(bytes("<html><head><title>PiVAC SERVER API</title></head>", "utf-8"))
            self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes("<p>Payload has not yet been loaded or can not be found. Please try again later or contact support</p>", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))

class startApi():
    def start():
    # if __name__ == "__main__":
        dt = datetime.now()
        ts = datetime.timestamp(dt)
        date_time = datetime.fromtimestamp(ts)
        utc_ts = date_time.strftime("%d-%m-%Y, %H:%M:%S")

        webServer = HTTPServer(server_address, MyServer)
        print("Server started http://%s:%s" % server_address, "@", utc_ts)

        try:
            print("it started for real")
            webServer.serve_forever()
        except KeyboardInterrupt:
            pass

        webServer.server_close()
        print("Server stopped.")
#####################################################################
# END WEB SERVER
