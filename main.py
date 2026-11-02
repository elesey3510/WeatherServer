import os
import time
import threading
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from recieveData import receive_packets
latest_data = {
    "humidity": 0.0,
    "temperature": 0.0,
    "pressure": 0.0,
    "lux": 0.0,
    "status": 0,
    "updated_at": 0
}
data_lock = threading.Lock()

class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory='public', **kwargs)
    def do_GET(self):
        if self.path == '/api/weather':
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            with data_lock:
                response_bytes = json.dumps(latest_data).encode('utf-8')
            self.wfile.write(response_bytes)
        else:
            super().do_GET()

def run_server():
    if not os.path.exists('public'):
        os.makedirs('public',exist_ok=True)
    server_address = ('',80)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print("\nHTTP STOP")
        httpd.server_close()
    httpd = HTTPServer(server_address,CustomHTTPRequestHandler)
if __name__ == "__main__":
    try:
        serial_thread = threading.Thread(target=receive_packets, daemon=True, args=(latest_data))
        serial_thread.start()

        receive_packets(latest_data)
    except KeyboardInterrupt:
        print("\nend")