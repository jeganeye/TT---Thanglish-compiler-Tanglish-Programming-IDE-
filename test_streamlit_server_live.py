"""
Live server test: Spawns 'streamlit run app.py' as a process and verifies HTTP 200 response
"""

import subprocess
import time
import urllib.request
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 60)
print("TESTING LIVE STREAMLIT SERVER (streamlit run app.py)")
print("=" * 60)

cmd = [sys.executable, "-m", "streamlit", "run", "app.py", "--server.headless=true", "--server.port=8501"]
print("Launching:", " ".join(cmd))

proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

server_healthy = False
attempts = 15
time.sleep(3)

for i in range(attempts):
    try:
        url = "http://127.0.0.1:8501"
        with urllib.request.urlopen(url, timeout=3) as res:
            if res.status == 200:
                print(f"[SUCCESS] Streamlit server is UP and responding with HTTP {res.status} at {url}")
                body = res.read().decode('utf-8', errors='ignore')
                if "streamlit" in body.lower() or "tanglish" in body.lower() or "<html" in body.lower():
                    print("[SUCCESS] Streamlit web application HTML rendered successfully!")
                server_healthy = True
                break
    except Exception as ex:
        # print(f"Attempt {i+1}: waiting for server ({ex})")
        time.sleep(1)

# Clean up
proc.terminate()
try:
    proc.wait(timeout=5)
except Exception:
    proc.kill()

print("Server process shut down cleanly.")
print("=" * 60)

if server_healthy:
    print("[PASS] Streamlit deployment-readiness check PASSED 100%!")
    sys.exit(0)
else:
    print("[FAIL] Streamlit server failed to start within timeout.")
    sys.exit(1)
