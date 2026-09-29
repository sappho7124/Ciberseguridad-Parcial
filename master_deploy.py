#!/usr/bin/env python3
import os
import sys
import shutil
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)  # Force execution inside the script directory

STEPS = [
    ("Step 1: Installing DNF Dependencies", "step1_install.py"),
    ("Step 2: Deploying Port 80 Forum Web Application", "step2_webapp.py"),
    ("Step 3: Creating Accounts & Sudoers Configurations", "step3_accounts.py"),
    ("Step 4: Building Honeypot Steganography Image", "step4_honeypot.py"),
    ("Step 5: Configuring Seasonal Profiles & Protected ZIPs", "step5_seasonal.py"),
    ("Step 6: Planting Root Flag & Unshadow Instructions", "step6_rootflag.py"),
    ("Step 7: Installing Network Auto-Healing Watchdog", "step7_network_watchdog.py"),
]

def main():
    if os.geteuid() != 0:
        print("[!] Error: This script must be run as root.")
        sys.exit(1)

    print("==================================================")
    print("      CTF PUZZLE MASTER DEPLOYMENT SUITE         ")
    print("==================================================")

    for title, script in STEPS:
        print(f"\n[*] Running: {title} ({script})...")
        result = subprocess.run([sys.executable, script])
        if result.returncode != 0:
            print(f"[!] ERROR: {script} failed with exit code {result.returncode}.")
            print("[!] Halting deployment. Fix error and re-run master or individual script.")
            sys.exit(1)
        print(f"[+] SUCCESS: {script} completed.")

    print("\n[*] Cleaning up deployment scripts and temporary files from host...")
    try:
        shutil.rmtree(SCRIPT_DIR)
        print("[+] Self-cleanup complete. Deployment folder removed.")
    except Exception as e:
        print(f"[!] Warning: Could not remove deployment directory: {e}")

    print("\n==================================================")
    print("[+] ALL DEPLOYMENT STEPS COMPLETED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    main()