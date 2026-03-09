#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import socket
import os

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Get pod information
        pod_name = os.environ.get('POD_NAME', 'unknown')
        namespace = os.environ.get('NAMESPACE', 'unknown')
        
        # Handle different endpoints
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            response = f"""
            <html>
            <body>
                <h1>Backend Server</h1>
                <p>Pod: {pod_name}</p>
                <p>Namespace: {namespace}</p>
                <p>Endpoint: /health - Health check</p>
                <p>Endpoint: /info - Pod information</p>
            </body>
            </html>
            """
            self.wfile.write(response.encode())
        
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK')
        
        elif self.path == '/info':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = f'{{"pod": "{pod_name}", "namespace": "{namespace}", "hostname": "{socket.gethostname()}"}}'
            self.wfile.write(response.encode())
        
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not Found')
    
    def log_message(self, format, *args):
        # Suppress log messages for cleaner output
        pass

def run_server(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHandler)
    print(f"Starting backend server on port {port}...")
    print(f"Pod name: {os.environ.get('POD_NAME', 'unknown')}")
    print(f"Namespace: {os.environ.get('NAMESPACE', 'unknown')}")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()