import subprocess
import time

# Start Flask web app
subprocess.Popen(["python", "web_app.py"])

# Start QR frontend (now handles ngrok itself)
subprocess.Popen(["python", "qr_front.py"])
time.sleep(3)

# Start Attendance UI
subprocess.Popen(["python", "SIH_test.py"])
