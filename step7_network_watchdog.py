#!/usr/bin/env python3
import os
import subprocess

SERVICE_NAME = "net-watchdog"

SERVICE_FILE = f'''[Unit]
Description=NetworkManager Auto-Healing Watchdog Service
After=network.target

[Service]
Type=simple
ExecStart=/bin/bash -c 'while true; do if ! ping -c 1 -W 2 192.168.56.1 >/dev/null 2>&1 && ! ping -c 1 -W 2 8.8.8.8 >/dev/null 2>&1; then echo "[$(date)] Network connection lost. Restarting NetworkManager..."; systemctl restart NetworkManager; sleep 10; fi; sleep 15; done'
Restart=always

[Install]
WantedBy=multi-user.target
'''

def main():
    service_path = f"/etc/systemd/system/{SERVICE_NAME}.service"
    with open(service_path, "w") as f:
        f.write(SERVICE_FILE)
        
    subprocess.run(["systemctl", "daemon-reload"], check=True)
    subprocess.run(["systemctl", "enable", "--now", SERVICE_NAME], check=True)
    print("[+] NetworkManager auto-healing watchdog service installed and active.")

if __name__ == "__main__":
    main()