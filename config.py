#!/usr/bin/env python3
import os

# Base Directory
BASE_DIR = "/opt/ctf_puzzle"

# Web Server Configuration (Port 80)
WEB_PORT = 80
WEB_SERVICE_NAME = "ctf-web"

# 5-Step CTF Progress Flags
FLAGS = {
    "FLAG1": "FLAG{1_sys_ssh_access_granted}",
    "FLAG2": "FLAG{2_root_privilege_escalation}",
    "FLAG3": "FLAG{3_unshadow_password_hash_cracked}",
    "FLAG4": "FLAG{4_zip_archive_pattern_unlocked}",
    "FLAG5": "FLAG{5_congrats_image_metadata_ctf_champion}"
}

# Honeypot User (Decoy)
HONEYPOT_USER = "dortega"
HONEYPOT_PASS = "mrortega"
HONEYPOT_IMG_NAME = "duck.jpg"
STEG_PASSPHRASE = "El pato contiene todos los secretos y esta es la llave"

# Updated clue instructing players to use pre-installed extraction tools
HONEYPOT_CLUE_TEXT = (
    f"{STEG_PASSPHRASE}\n\n"
    f"Psssss Usa 'unzip {HONEYPOT_IMG_NAME}' o '7z x {HONEYPOT_IMG_NAME}'\n"
)

STEG_MESSAGE = "El pato es un mentiroso, esto era una trampa para hacerte perder el tiempo, busca a un tal herrera"

# Vulnerable User (Sudo Privilege Escalation)
VULN_USER = "nherrera"
VULN_PASS = "BLACKBOX"  # Embedded in website content for cewl

# ==============================================================================
# EDITABLE PLAYER-FACING TEXT & CLUES
# ==============================================================================

# Initial SSH access text (/home/nherrera/readme.txt & flag1)
SYS_ADMIN_README_TEXT = "Se otorgaron permisos extra de python para mantenimiento.\n"
FLAG1_TEXT = f"{FLAGS['FLAG1']}\n\nFelicidades, lograste entrar toma tu bandera\n"

# Root level instructions file (/root/flag2_root_access.txt)
ROOT_INSTRUCTIONS_TEXT = f"""
Entra al perfil asignado a la fecha de tu nacimiento desvelando las sombras, tu amigo john te podra ayudar

Mrspring/Enero - Marzo
Mssummer/Abril - Junio
Msautumn/Julio - Septiembre
Mrwinter/Octubre - Diciembre
"""

# ==============================================================================
# SEASONAL ACCOUNTS CONFIGURATION
# ==============================================================================
SEASONAL_IMG_NAME = "felicitaciones.jpg"

FLAG2_TEXT = f"{FLAGS['FLAG2']}\n\nEscucha la voz de las raices\n"
FLAG3_TEXT = f"{FLAGS['FLAG3']}\n\nAdquiere los archivos del zip\n"
FLAG4_TEXT = f"{FLAGS['FLAG4']}\n\n{SEASONAL_IMG_NAME} Contiene la ultima bandera, buscala y sera el final\n"

SEASONAL_ACCOUNTS = {
    "Mrspring": {
        "pass": "sunshine",
        "months": "Enero - Marzo",
        "zip_pass": "abS123",
        "zip_clue": "6 simbolos: 2 minusculas, seguido de mayuscula 'S', seguido de 3 digitos (0-9)."
    },
    "Mssummer": {
        "pass": "summer2022",
        "months": "Abril - Junio",
        "zip_pass": "xyZ999",
        "zip_clue": "6 simbolos: 2 minusculas, seguido de mayuscula 'Z', seguido de 3 digitos (0-9)."
    },
    "Msautumn": {
        "pass": "pumpkin",
        "months": "Julio - Septiembre",
        "zip_pass": "cdK456",
        "zip_clue": "6 simbolos: 2 minusculas, seguido de mayuscula 'K', seguido de 3 digitos (0-9)."
    },
    "Mrwinter": {
        "pass": "winter2024",
        "months": "Octubre - Diciembre",
        "zip_pass": "efM789",
        "zip_clue": "6 simbolos: 2 minusculas, seguido de mayuscula 'M', seguido de 3 digitos (0-9)."
    }
}