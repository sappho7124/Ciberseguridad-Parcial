#!/usr/bin/env python3
import os
import sys
import shutil
import subprocess
from config import BASE_DIR, WEB_PORT, WEB_SERVICE_NAME

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TARGET_WEB_DIR = os.path.join(BASE_DIR, "web")

SERVICE_FILE = f'''[Unit]
Description=CTF Forum Web Application
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory={TARGET_WEB_DIR}
ExecStart=/usr/bin/python3 -m http.server {WEB_PORT} --directory {TARGET_WEB_DIR}
Restart=always

[Install]
WantedBy=multi-user.target
'''

def configure_firewall():
    print("[*] Opening Port 80 in firewalld...")
    subprocess.run(["firewall-cmd", "--add-service=http", "--permanent"], capture_output=True)
    subprocess.run(["firewall-cmd", "--add-port=80/tcp", "--permanent"], capture_output=True)
    subprocess.run(["firewall-cmd", "--reload"], capture_output=True)

def main():
    os.makedirs(TARGET_WEB_DIR, exist_ok=True)
    local_web_dir = os.path.join(SCRIPT_DIR, "web")

    if os.path.exists(local_web_dir) and os.path.isdir(local_web_dir):
        shutil.copytree(local_web_dir, TARGET_WEB_DIR, dirs_exist_ok=True)
    else:
        # Copy all web files directly from the current directory
        web_extensions = ('.html', '.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.txt')
        for fname in os.listdir(SCRIPT_DIR):
            if fname.lower().endswith(web_extensions) and not fname.startswith("step"):
                src = os.path.join(SCRIPT_DIR, fname)
                dst = os.path.join(TARGET_WEB_DIR, fname)
                shutil.copy2(src, dst)

    service_path = f"/etc/systemd/system/{WEB_SERVICE_NAME}.service"
    with open(service_path, "w") as f:
        f.write(SERVICE_FILE)

    subprocess.run(["systemctl", "daemon-reload"], check=True)
    subprocess.run(["systemctl", "enable", "--now", WEB_SERVICE_NAME], check=True)
    
    # Enable firewall traffic
    configure_firewall()
    
    print(f"[+] Web application deployed to {TARGET_WEB_DIR} and live on Port {WEB_PORT}.")

if __name__ == "__main__":
    main()