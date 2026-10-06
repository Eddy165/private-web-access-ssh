import json
import subprocess
import sys
import time
import urllib.request
import urllib.error

p = subprocess.Popen([sys.executable, "private_web/server.py"])
try:
    last_error = None
    for _ in range(20):
        try:
            body = urllib.request.urlopen("http://127.0.0.1:8000/health", timeout=1).read()
            if body == b"OK":
                break
        except Exception as exc:
            last_error = exc
            time.sleep(0.25)
    else:
        raise RuntimeError(f"Server did not become ready: {last_error}")

    data = json.loads(
        urllib.request.urlopen("http://127.0.0.1:8000/api/status", timeout=3).read()
    )
    assert data["status"] == "online"
    assert data["bound_address"] == "127.0.0.1"
    print("PASS: private web server health and status endpoints")
finally:
    p.terminate()
    try:
        p.wait(timeout=5)
    except subprocess.TimeoutExpired:
        p.kill()
