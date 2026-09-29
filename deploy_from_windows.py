import os
import sys

# Install paramiko automatically if missing
try:
    import paramiko
except ImportError:
    print("[*] Installing paramiko for SSH/SFTP management...")
    os.system(f"{sys.executable} -m pip install paramiko")
    import paramiko

def load_env(env_path=".env"):
    config = {}
    if not os.path.exists(env_path):
        print(f"[!] Error: {env_path} file not found!")
        sys.exit(1)
    with open(env_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                config[k.strip()] = v.strip()
    return config

def upload_dir(sftp, local_path, remote_path):
    try:
        sftp.mkdir(remote_path)
    except IOError:
        pass  # Directory already exists

    for item in os.listdir(local_path):
        # Skip deployment control files and hidden directories
        if item in [".env", "deploy_from_windows.py", ".git", "__pycache__"]:
            continue

        l_item = os.path.join(local_path, item)
        r_item = f"{remote_path}/{item}".replace("\\", "/")

        if os.path.isdir(l_item):
            upload_dir(sftp, l_item, r_item)
        else:
            print(f"[-->] Syncing: {item}")
            sftp.put(l_item, r_item)

def main():
    cfg = load_env()
    ip = cfg.get("TARGET_IP")
    user = cfg.get("TARGET_USER", "root")
    password = cfg.get("TARGET_PASS")
    remote_dir = cfg.get("REMOTE_DIR", "/root/ctf_deploy")

    print(f"[*] Connecting to {user}@{ip}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(ip, username=user, password=password, timeout=10)
    except Exception as e:
        print(f"[!] SSH Connection failed: {e}")
        sys.exit(1)

    print("[*] Uploading/Syncing local files to Fedora...")
    sftp = ssh.open_sftp()
    upload_dir(sftp, ".", remote_dir)
    sftp.close()

    print("\n[*] Executing remote master setup...")
    cmd = f"python3 {remote_dir}/master_deploy.py"
    stdin, stdout, stderr = ssh.exec_command(cmd)

    # Stream remote output live to Windows terminal
    for line in iter(stdout.readline, ""):
        print(line, end="")
    
    err = stderr.read().decode()
    if err:
        print(f"\n[!] Remote Errors:\n{err}")

    ssh.close()
    print("\n[+] Deployment process finished.")

if __name__ == "__main__":
    main()