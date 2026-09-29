#!/usr/bin/env python3
import os
import shutil
import subprocess
from PIL import Image, ImageDraw, PngImagePlugin
from config import SEASONAL_ACCOUNTS, SEASONAL_IMG_NAME, FLAGS, FLAG3_TEXT, FLAG4_TEXT

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(SCRIPT_DIR, "assets")
CTF_TAG = "CTF_MANAGED"

def set_user(username, password):
    res = subprocess.run(["id", username], capture_output=True)
    if res.returncode != 0:
        subprocess.run(["useradd", "-m", "-s", "/bin/bash", "-c", CTF_TAG, username], check=True)
    else:
        subprocess.run(["usermod", "-c", CTF_TAG, username], capture_output=True)

    chpasswd_proc = subprocess.Popen(["chpasswd"], stdin=subprocess.PIPE, text=True)
    chpasswd_proc.communicate(f"{username}:{password}\n")

def get_custom_congrats_image():
    if os.path.exists(ASSETS_DIR):
        for ext in [".jpg", ".jpeg", ".png"]:
            for fname in os.listdir(ASSETS_DIR):
                if fname.lower().startswith("congrats") and fname.lower().endswith(ext):
                    return os.path.join(ASSETS_DIR, fname)
    return None

def embed_flag5_into_image(src_path, dst_path):
    if src_path and os.path.exists(src_path):
        img = Image.open(src_path)
    else:
        img = Image.new('RGB', (600, 250), color=(34, 139, 34))
        d = ImageDraw.Draw(img)
        d.text((30, 100), "Congratulations! Challenge Completed!", fill=(255, 255, 255))

    if dst_path.lower().endswith(".png"):
        meta = PngImagePlugin.PngInfo()
        meta.add_text("Comment", FLAGS["FLAG5"])
        img.save(dst_path, pnginfo=meta)
    else:
        img.save(dst_path, comment=FLAGS["FLAG5"].encode("utf-8"))

def main():
    custom_img = get_custom_congrats_image()

    for username, data in SEASONAL_ACCOUNTS.items():
        set_user(username, data["pass"])
        user_home = os.path.expanduser(f"~{username}")

        # Plant Flag 3 text file
        with open(os.path.join(user_home, "flag3_account_cracked.txt"), "w") as f:
            f.write(FLAG3_TEXT)

        # Plant Flag 4 text file to be zipped
        flag4_temp_path = os.path.join(user_home, "flag4_zip_unlocked.txt")
        with open(flag4_temp_path, "w") as f:
            f.write(FLAG4_TEXT)

        # Build image with Flag 5 embedded in metadata
        img_path = os.path.join(user_home, SEASONAL_IMG_NAME)
        embed_flag5_into_image(custom_img, img_path)

        # Create password-protected ZIP archive
        zip_path = os.path.join(user_home, "flag_archive.zip")
        if os.path.exists(zip_path):
            os.remove(zip_path)

        subprocess.run([
            "zip", "-j", "-P", data["zip_pass"], zip_path, flag4_temp_path, img_path
        ], check=True)

        # Remove raw files from home folder
        os.remove(flag4_temp_path)
        os.remove(img_path)

        # Write pattern clue file
        with open(os.path.join(user_home, "zip_password_clue.txt"), "w") as f:
            f.write(f"Seasonal Profile Quarters: {data['months']}\n")
            f.write(f"ZIP Password Pattern Clue: {data['zip_clue']}\n")

        subprocess.run(["chown", "-R", f"{username}:{username}", user_home])

    print("[+] Seasonal profiles updated with Flags 3, 4, and 5 successfully planted.")

if __name__ == "__main__":
    main()