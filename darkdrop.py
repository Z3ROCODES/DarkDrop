import os
import subprocess
import time
from flask import Flask, send_from_directory

app = Flask(__name__, static_folder='Files')

@app.route('/')
def index():
    return send_from_directory('Files', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('Files', filename)

def create_hidden_service():
    hidden_service_dir = 'hidden_service'
    os.makedirs(hidden_service_dir, exist_ok=True)

    torrc_content = f'''
HiddenServiceDir {os.path.abspath(hidden_service_dir)}
HiddenServicePort 80 127.0.0.1:5000
Log notice stdout
'''
    with open('torrc.temp', 'w') as f:
        f.write(torrc_content)

def start_tor():
    print("[*] Starting Tor...")
    return subprocess.Popen(
        [r'C:\Users\fadin\Desktop\Tor Browser\Browser\TorBrowser\Tor\tor.exe', '-f', 'torrc.temp'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

create_hidden_service()
tor_process = start_tor()

print("[*] Waiting for Tor to generate .onion address...")
while not os.path.exists('hidden_service/hostname'):
    time.sleep(1)

with open('hidden_service/hostname', 'r') as f:
    onion_address = f.read().strip()

print(f"[+] Your .onion URL: http://{onion_address}")

print("[*] Starting Flask web server...")
app.run(host='127.0.0.1', port=5000)
