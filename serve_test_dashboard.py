#!/usr/bin/env python
"""
🌐 Simple HTTP Server for Backend Test Dashboard
"""

import http.server
import socketserver
from pathlib import Path
import os

PORT = 3000
HANDLER = http.server.SimpleHTTPRequestHandler

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/backend_test.html'
        return super().do_GET()

os.chdir(Path(__file__).parent)

print("\n" + "="*70)
print("🌐 Backend Test Dashboard")
print("="*70)
print(f"\n📍 Access at: http://localhost:{PORT}")
print("\nFeatures:")
print("  ✓ System status check")
print("  ✓ API endpoint testing")
print("  ✓ Live response display")
print("  ✓ Auto-refresh every 5 seconds")
print("\nPress Ctrl+C to stop")
print("="*70 + "\n")

try:
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"✅ Server running on http://localhost:{PORT}")
        print("Opening in browser...\n")
        os.system(f"start http://localhost:{PORT}")
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\n\n⛔ Server stopped")
except Exception as e:
    print(f"\n❌ Error: {e}")
