#!/usr/bin/env bash
echo "[*] Instalando Dox Kit..."
if command -v pkg >/dev/null; then
    pkg install python dnsutils whois git -y
else
    sudo apt install python3 python3-pip dnsutils whois git -y
fi
python -m pip install --quiet phonenumbers 2>/dev/null || echo "[i] phonenumbers opcional no instalado"
chmod +x dox
echo "[+] Listo. Ejecuta: ./dox"