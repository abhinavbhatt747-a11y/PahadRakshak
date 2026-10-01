import sys
import time
from pyngrok import ngrok

print("[+] Starting HTTPS Secure Tunnel for Real Mobile Hardware GPS Access...")
try:
    tunnel = ngrok.connect(8000)
    print("\n" + "="*60)
    print(f"🔒 REAL MOBILE HARDWARE GPS HTTPS URL:")
    print(f"👉 {tunnel.public_url}/app/map.html")
    print(f"👉 Citizen App: {tunnel.public_url}/app/citizen.html")
    print("="*60 + "\n")
    print("[!] Open the HTTPS link above on your mobile phone browser!")
    print("[!] Mobile Chrome/Safari will prompt for REAL HARDWARE GPS permissions!")

    while True:
        time.sleep(1)
except Exception as e:
    print(f"[!] Tunnel Error: {e}")
