from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from datetime import datetime
import json
import os
import platform
import socket

HOST = os.getenv("PRIVATE_WEB_HOST", "127.0.0.1")
PORT = int(os.getenv("PRIVATE_WEB_PORT", "8000"))
STATIC_DIR = Path(__file__).parent / "static"

class Handler(BaseHTTPRequestHandler):
    server_version = "PrivateWebDemo/1.0"

    def _send(self, status, body, content_type="text/html; charset=utf-8"):
        data = body if isinstance(body, bytes) else body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/":
            self._send(200, (STATIC_DIR / "index.html").read_bytes())
        elif self.path == "/api/status":
            payload = {
                "service": "Private Web Access Demo",
                "status": "online",
                "server_hostname": socket.gethostname(),
                "server_os": platform.system(),
                "bound_address": HOST,
                "private_port": PORT,
                "time": datetime.now().isoformat(timespec="seconds"),
                "security_note": "This service is intended to be reached through an SSH local port-forward."
            }
            self._send(200, json.dumps(payload, indent=2), "application/json; charset=utf-8")
        elif self.path == "/health":
            self._send(200, "OK", "text/plain; charset=utf-8")
        else:
            self._send(404, "Not Found", "text/plain; charset=utf-8")

    def log_message(self, fmt, *args):
        print(f"[WEB] {self.client_address[0]} - {fmt % args}")

if __name__ == "__main__":
    print("=" * 62)
    print(" PRIVATE WEB ACCESS USING SSH PORT FORWARDING")
    print("=" * 62)
    print(f"Private service: http://{HOST}:{PORT}")
    print("The service is loopback-only by default.")
    print("Press Ctrl+C to stop.")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
