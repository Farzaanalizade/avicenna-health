#!/usr/bin/env python
"""
⚡ Ultra-Simple Backend Test Server
"""

import http.server
import socketserver
from pathlib import Path
import os
import json

PORT = 8888

class TestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            
            html = open(Path(__file__).parent / 'backend_test.html', 'rb').read()
            self.wfile.write(html)
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass  # Suppress logging

os.chdir(Path(__file__).parent)

print(f"\n✅ Test Dashboard: http://localhost:{PORT}\n")

try:
    with socketserver.TCPServer(("", PORT), TestHandler) as httpd:
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\n\n⛔ Server stopped\n")
except Exception as e:
    print(f"\n❌ Error: {e}\n")
