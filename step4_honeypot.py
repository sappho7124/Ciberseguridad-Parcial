#!/usr/bin/env python3
import os
import shutil
import subprocess
from PIL import Image, ImageDraw
from config import (
    HONEYPOT_USER, STEG_PASSPHRASE, STEG_MESSAGE, 
    HONEYPOT_IMG_NAME, HONEYPOT_CLUE_TEXT
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(SCRIPT_DIR, "assets")

def get_custom_cover():
    if os.path.exists(ASSETS_DIR):
        for ext in [".jpg", ".jpeg", ".bmp"]:
            for fname in os.listdir(ASSETS_DIR):
                if fname.lower().startswith("cover") and fname.lower().endswith(ext):
                    return os.path.join(ASSETS_DIR, fname)
    return None

def main():
    user_home = os.path.expanduser(f"~{HONEYPOT_USER}")
    img_path = os.path.join(user_home, HONEYPOT_IMG_NAME)
    msg_path = os.path.join(user_home, "secret.txt")
    zip_path = os.path.join(user_home, "payload.zip")
    clue_path = os.path.join(user_home, "clue.txt")

    custom_cover = get_custom_cover()

    # 1. Copy custom image asset or generate base image
    if custom_cover:
        shutil.copy(custom_cover, img_path)
    else:
        img = Image.new('RGB', (400, 400), color=(73, 109, 137))
        d = ImageDraw.Draw(img)
        d.text((20, 180), "Honeypot Decoy Image", fill=(255, 255, 0))
        img.save(img_path)

    # 2. Write decoy secret text message
    with open(msg_path, "w") as f:
        f.write(STEG_MESSAGE + "\n")

    # 3. Encrypt secret.txt into a temporary password-protected ZIP
    subprocess.run([
        "zip", "-j", "-P", STEG_PASSPHRASE, zip_path, msg_path
    ], check=True)

    # 4. Create Polyglot: Append encrypted ZIP payload directly onto JPEG binary
    with open(img_path, "ab") as f_img, open(zip_path, "rb") as f_zip:
        f_img.write(f_zip.read())

    # 5. Write player clue file
    with open(clue_path, "w") as f:
        f.write(HONEYPOT_CLUE_TEXT)

    # Clean up unencrypted temporary files from target system
    if os.path.exists(msg_path):
        os.remove(msg_path)
    if os.path.exists(zip_path):
        os.remove(zip_path)

    subprocess.run(["chown", "-R", f"{HONEYPOT_USER}:{HONEYPOT_USER}", user_home])
    print(f"[+] Polyglot image '{HONEYPOT_IMG_NAME}' deployed successfully.")

if __name__ == "__main__":
    main()