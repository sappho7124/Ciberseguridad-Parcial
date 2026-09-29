#!/usr/bin/env python3
import os
from config import FLAG2_TEXT, ROOT_INSTRUCTIONS_TEXT

def main():
    flag2_path = "/root/flag2_root_access.txt"
    root_txt_path = "/root/root.txt"

    # Remove any existing symlinks or old files to ensure fresh, separate files
    for path in [flag2_path, root_txt_path]:
        if os.path.lexists(path):
            os.remove(path)

    # 1. File 1: Dedicated Flag 2 file
    with open(flag2_path, "w") as f:
        f.write(FLAG2_TEXT)
    os.chmod(flag2_path, 0o600)

    # 2. File 2: Separate Root Instructions file
    with open(root_txt_path, "w") as f:
        f.write(ROOT_INSTRUCTIONS_TEXT)
    os.chmod(root_txt_path, 0o600)

    print("[+] Created separate root files: '/root/flag2_root_access.txt' and '/root/root.txt'.")

if __name__ == "__main__":
    main()