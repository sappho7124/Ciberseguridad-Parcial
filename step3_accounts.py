#!/usr/bin/env python3
import os
import pwd
import subprocess
from config import (
    HONEYPOT_USER, HONEYPOT_PASS, VULN_USER, VULN_PASS, 
    SEASONAL_ACCOUNTS, SYS_ADMIN_README_TEXT, FLAG1_TEXT
)

CTF_TAG = "CTF_MANAGED"

def get_allowed_users():
    allowed = {HONEYPOT_USER, VULN_USER}
    allowed.update(SEASONAL_ACCOUNTS.keys())
    return allowed

def cleanup_obsolete_users():
    allowed_users = get_allowed_users()
    for user_entry in pwd.getpwall():
        username = user_entry.pw_name
        gecos = user_entry.pw_gecos

        if gecos == CTF_TAG and username not in allowed_users:
            sudoers_file = f"/etc/sudoers.d/{username}"
            if os.path.exists(sudoers_file):
                os.remove(sudoers_file)
            subprocess.run(["pkill", "-u", username], capture_output=True)
            subprocess.run(["userdel", "-r", "-f", username], capture_output=True)

def set_user(username, password):
    res = subprocess.run(["id", username], capture_output=True)
    if res.returncode != 0:
        subprocess.run(["useradd", "-m", "-s", "/bin/bash", "-c", CTF_TAG, username], check=True)
    else:
        subprocess.run(["usermod", "-c", CTF_TAG, username], capture_output=True)

    chpasswd_proc = subprocess.Popen(["chpasswd"], stdin=subprocess.PIPE, text=True)
    chpasswd_proc.communicate(f"{username}:{password}\n")

def main():
    cleanup_obsolete_users()

    set_user(HONEYPOT_USER, HONEYPOT_PASS)
    set_user(VULN_USER, VULN_PASS)

    # Configure Sudo Misconfiguration for sys_admin
    sudoers_path = f"/etc/sudoers.d/{VULN_USER}"
    with open(sudoers_path, "w") as f:
        f.write(f"{VULN_USER} ALL=(ALL) NOPASSWD: /usr/bin/python3\n")
    os.chmod(sudoers_path, 0o440)

    # Plant text files into sys_admin's home directory
    vuln_home = os.path.expanduser(f"~{VULN_USER}")
    
    with open(os.path.join(vuln_home, "readme.txt"), "w") as f:
        f.write(SYS_ADMIN_README_TEXT)

    with open(os.path.join(vuln_home, "flag1_initial_access.txt"), "w") as f:
        f.write(FLAG1_TEXT)

    subprocess.run(["chown", "-R", f"{VULN_USER}:{VULN_USER}", vuln_home])
    print("[+] Main accounts configured and Flag 1 planted.")

if __name__ == "__main__":
    main()