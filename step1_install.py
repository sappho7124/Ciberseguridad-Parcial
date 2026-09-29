#!/usr/bin/env python3
import os
import subprocess
import sys

# DNF packages required for puzzle runtime and tools
REQUIRED_PACKAGES = [
    "python3",
    "python3-pillow",
    "zip",
    "unzip",
    "firewalld"
]

def configure_ssh_for_bruteforce():
    print("[*] Tuning OpenSSH configuration to permit Hydra brute-force attempts...")
    sshd_conf_dir = "/etc/ssh/sshd_config.d"
    os.makedirs(sshd_conf_dir, exist_ok=True)
    conf_path = os.path.join(sshd_conf_dir, "99-ctf-bruteforce.conf")

    ssh_config_content = """# CTF Brute-Force Rate Limit Tuning
MaxStartups 100:30:100
MaxAuthTries 100
PerSourceMaxStartups 100
"""

    with open(conf_path, "w") as f:
        f.write(ssh_config_content)

    # Reload OpenSSH service
    subprocess.run(["systemctl", "restart", "sshd"], check=True)
    print("[+] OpenSSH configured: MaxStartups & MaxAuthTries raised.")

def main():
    if os.geteuid() != 0:
        print("[!] Error: This script must be run as root.")
        sys.exit(1)

    print("[*] Installing system package dependencies via DNF...")
    cmd = ["dnf", "install", "-y"] + REQUIRED_PACKAGES
    result = subprocess.run(cmd)

    if result.returncode != 0:
        print("[!] Warning: Some packages failed to install. Retrying with --skip-broken...")
        subprocess.run(["dnf", "install", "-y", "--skip-broken"] + REQUIRED_PACKAGES)

    # Inject SSH tuning settings
    configure_ssh_for_bruteforce()

    print("[+] System dependencies and SSH configuration completed.")

if __name__ == "__main__":
    main()