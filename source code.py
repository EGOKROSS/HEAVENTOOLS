import os
import sys
import time
import random
import socket
import string
import secrets
import hashlib
import base64
import subprocess
import requests
from colorama import init

# Initialize colorama
init(autoreset=True)

# Cross-platform clear command
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Force Windows Terminal to use UTF-8 (Fixes block characters)
if os.name == 'nt':
    os.system('chcp 65001 >nul')

# --- ANSI COLORS ---
WHITE = "\033[1;37m"
DIM_WHITE = "\033[37m"
GRAY = "\033[90m"
DARK_GRAY = "\033[1;30m"
BLACK = "\033[30m"
RED = "\033[1;31m"
GREEN = "\033[1;32m"
RESET = "\033[0m"

PROMPT = WHITE + "heaven@tools:~# " + RESET

# THE 3D BLOCK BANNER
BANNER_STR = r"""
  ██╗  ██╗███████╗ █████╗ ██╗   ██╗███████╗███╗   ██╗
  ██║  ██║██╔════╝██╔══██╗██║   ██║██╔════╝████╗  ██║
  ███████║█████╗  ███████║██║   ██║█████╗  ██╔██╗ ██║
  ██╔══██║██╔══╝  ██╔══██║╚██╗ ██╔╝██╔══╝  ██║╚██╗██║
  ██║  ██║███████╗██║  ██║ ╚████╔╝ ███████╗██║ ╚████║
  ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═══╝
  
  ████████╗ ██████╗  ██████╗ ██╗     ███████╗
  ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
     ██║   ██║   ██║██║   ██║██║     ███████╗
     ██║   ██║   ██║██║   ██║██║     ╚════██║
     ██║   ╚██████╔╝╚██████╔╝███████╗███████║
     ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
"""

def type_print(text, speed=0.002):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print() 

def print_banner():
    clear_screen()
    for line in BANNER_STR.split('\n'):
        if line.strip():
            type_print(WHITE + line + RESET, speed=0.001)

    max_width = max(len(line) for line in BANNER_STR.split('\n')) if BANNER_STR else 1
    drip_chars = ['█', '▓', '▒', '░', '│']
    drips = [""] * max_width
    
    for x in range(max_width):
        if random.random() < 0.4:
            drips[x] = "".join([random.choice(drip_chars) for _ in range(random.randint(2, 6))])
            
    for depth in range(6):
        drip_line = ""
        for x in range(max_width):
            if len(drips[x]) > depth:
                color = DIM_WHITE if depth < 2 else GRAY if depth < 4 else DARK_GRAY
                drip_line += f"{color}{drips[x][depth]}"
            else:
                drip_line += " "
        if drip_line.strip():
            type_print(drip_line + RESET, speed=0.001)

    type_print("\n" + WHITE + "=" * 65, speed=0.001)
    type_print(WHITE + "            HEAVENTOOLS: NETWORK & WEB SUITE", speed=0.001)
    type_print(WHITE + "=" * 65 + "\n", speed=0.001)

def ip_lookup():
    print(WHITE + "[*] Enter an IP address (leave blank for your own IP):")
    ip = input(PROMPT).strip()
    try:
        data = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
        if data.get("status") == "fail":
            print(RED + f"[-] Error: {data.get('message')}\n")
            return
        print(WHITE + "-" * 40)
        print(WHITE + f" IP:          {data.get('query')}")
        print(WHITE + f" Country:     {data.get('country')} ({data.get('countryCode')})")
        print(WHITE + f" Region:      {data.get('regionName')}")
        print(WHITE + f" City:        {data.get('city')}")
        print(WHITE + f" ISP:         {data.get('isp')}")
        print(WHITE + f" Org:         {data.get('org')}")
        print(WHITE + f" Coords:      {data.get('lat')}, {data.get('lon')}")
        print(WHITE + "-" * 40 + "\n")
    except requests.exceptions.RequestException:
        print(RED + "[-] Network Error: Could not connect to API.\n")

def reverse_dns():
    print(WHITE + "[*] Enter an IP to find its hostname:")
    ip = input(PROMPT).strip()
    try:
        hostname = socket.gethostbyaddr(ip)
        print(WHITE + f"\n[+] IP: {ip}")
        print(WHITE + f"[+] Hostname: {hostname[0]}")
        print(WHITE + f"[+] Aliases: {', '.join(hostname[1]) if hostname[1] else 'None'}\n")
    except socket.herror:
        print(RED + "\n[-] Error: No hostname found for this IP.\n")

def port_scanner():
    print(WHITE + "[*] Enter target IP or Domain:")
    target = input(PROMPT).strip()
    print(WHITE + "\n[*] Scanning common ports...\n")
    common_ports = [21, 22, 80, 443, 3306, 8080, 1337]
    try:
        target_ip = socket.gethostbyname(target)
        print(WHITE + f"[*] Target IP: {target_ip}\n")
        for port in common_ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            if s.connect_ex((target_ip, port)) == 0:
                print(GREEN + f" [+] Port {port} is OPEN")
            else:
                print(DIM_WHITE + f" [-] Port {port} is closed")
            s.close()
        print("\n")
    except socket.gaierror:
        print(RED + "[-] Error: Could not resolve host.\n")

def ping_target():
    print(WHITE + "[*] Enter IP or Domain to ping:")
    target = input(PROMPT).strip()
    print(WHITE + f"\n[*] Pinging {target}...\n")
    try:
        if os.name == 'nt':
            output = subprocess.check_output(f"ping -n 4 {target}", shell=True, text=True)
        else:
            output = subprocess.check_output(f"ping -c 4 {target}", shell=True, text=True)
        print(WHITE + output + "\n")
    except Exception:
        print(RED + "[-] Ping failed. Host unreachable.\n")

def dns_lookup():
    print(WHITE + "[*] Enter a domain (e.g., google.com):")
    domain = input(PROMPT).strip()
    try:
        ip = socket.gethostbyname(domain)
        print(WHITE + f"\n[+] Domain: {domain}")
        print(WHITE + f"[+] Resolves to IP: {ip}\n")
    except socket.gaierror:
        print(RED + "\n[-] Error: Could not resolve domain.\n")

def cookie_inspector():
    print(WHITE + "[*] Enter a website URL to inspect its cookies:")
    url = input(PROMPT).strip()
    if not url.startswith("http"): url = "https://" + url
    print(WHITE + "\n[*] Fetching cookies from headers...\n")
    try:
        session = requests.Session()
        session.get(url, timeout=5)
        if not session.cookies:
            print(DIM_WHITE + " [-] No cookies found on this site.\n")
        else:
            print(GREEN + f"[+] Found {len(session.cookies)} cookies:")
            for cookie in session.cookies:
                secure_flag = "SECURE" if cookie.secure else "INSECURE"
                httponly_flag = "HTTPONLY" if cookie.has_nonstandard_attr('HttpOnly') else "JS-ACCESSIBLE"
                print(WHITE + f" {cookie.name.ljust(20)} : {str(cookie.value)[:30]}...")
                print(GRAY + f"   Flags: {secure_flag} | {httponly_flag}")
            print("\n")
    except Exception:
        print(RED + "[-] Error: Could not connect to website.\n")

def robots_txt():
    print(WHITE + "[*] Enter a domain to scrape Robots.txt:")
    url = input(PROMPT).strip()
    if not url.startswith("http"): url = "https://" + url
    try:
        r = requests.get(f"{url}/robots.txt", timeout=5)
        if r.status_code == 200:
            print(WHITE + "\n" + "-" * 40)
            print(WHITE + r.text[:500] + ("\n...[truncated]" if len(r.text) > 500 else ""))
            print(WHITE + "-" * 40 + "\n")
        else:
            print(RED + f"\n[-] No robots.txt found (Status: {r.status_code})\n")
    except Exception:
        print(RED + "[-] Error connecting to website.\n")

def tech_detect():
    print(WHITE + "[*] Enter a website URL to detect its Tech Stack:")
    url = input(PROMPT).strip()
    if not url.startswith("http"): url = "https://" + url
    print(WHITE + "\n[*] Analyzing headers...\n")
    try:
        r = requests.get(url, timeout=5)
        headers = r.headers
        print(WHITE + "-" * 40)
        print(WHITE + f" Server:       {headers.get('Server', 'Unknown')}")
        print(WHITE + f" Powered By:   {headers.get('X-Powered-By', 'Unknown')}")
        print(WHITE + f" Cloudflare:   {'Yes' if 'cloudflare' in headers.get('Server', '').lower() else 'No'}")
        print(WHITE + "-" * 40 + "\n")
    except Exception:
        print(RED + "[-] Error connecting to website.\n")

def header_grabber():
    print(WHITE + "[*] Enter a website URL:")
    url = input(PROMPT).strip()
    if not url.startswith("http"): url = "https://" + url
    print(WHITE + "\n[*] Fetching server headers...\n")
    try:
        r = requests.head(url, timeout=5, allow_redirects=True)
        print(WHITE + f"[*] Status Code: {r.status_code}\n")
        for key, value in r.headers.items():
            print(WHITE + f" {key}: {value}")
        print("\n")
    except requests.exceptions.RequestException:
        print(RED + "[-] Error: Could not connect to server.\n")

def link_unshortener():
    print(WHITE + "[*] Enter a shortened URL (bit.ly, t.co, etc.):")
    url = input(PROMPT).strip()
    if not url.startswith("http"): url = "https://" + url
    print(WHITE + "\n[*] Tracing redirects...\n")
    try:
        r = requests.head(url, timeout=5, allow_redirects=True)
        print(GREEN + f"[*] Final Destination:\n -> {r.url}\n")
    except Exception:
        print(RED + "[-] Error tracing link.\n")

def base64_tool():
    print(WHITE + "[1] Encode Text  [2] Decode Base64")
    choice = input(PROMPT).strip()
    if choice == "1":
        text = input(WHITE + "Enter text: ").strip()
        print(GREEN + f"\n[+] Encoded: {base64.b64encode(text.encode()).decode()}\n")
    elif choice == "2":
        text = input(WHITE + "Enter Base64: ").strip()
        try:
            print(GREEN + f"\n[+] Decoded: {base64.b64decode(text).decode()}\n")
        except:
            print(RED + "\n[-] Invalid Base64 string.\n")

def hash_generator():
    print(WHITE + "[*] Enter a string to hash:")
    text = input(PROMPT).strip()
    if not text: return
    print(WHITE + "\n[*] Generating hashes...\n")
    print(WHITE + f" MD5:    {hashlib.md5(text.encode()).hexdigest()}")
    print(WHITE + f" SHA1:   {hashlib.sha1(text.encode()).hexdigest()}")
    print(WHITE + f" SHA256: {hashlib.sha256(text.encode()).hexdigest()}\n")

def password_generator():
    print(WHITE + "[*] How long should the password be? (Default 16):")
    length_str = input(PROMPT).strip()
    length = int(length_str) if length_str.isdigit() else 16
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(chars) for _ in range(length))
    print(GREEN + f"\n[+] Generated Password: \n -> {password}\n")

def subdomain_scanner():
    print(WHITE + "[*] Enter a domain to scan for subdomains (e.g., example.com):")
    domain = input(PROMPT).strip()
    subdomains = ["www", "mail", "api", "dev", "blog", "admin", "vpn", "test", "shop", "ftp"]
    print(WHITE + f"\n[*] Scanning {len(subdomains)} common subdomains for {domain}...\n")
    found = 0
    for sub in subdomains:
        target = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(target)
            print(GREEN + f" [+] FOUND: {target.ljust(25)} -> {ip}")
            found += 1
        except socket.gaierror:
            pass 
    if found == 0:
        print(DIM_WHITE + " [-] No common subdomains found.\n")
    else:
        print("\n")

def main():
    print_banner()
    while True:
        print(WHITE + " [IP & NETWORK]            [WEBSITE & WEB]")
        print(WHITE + " 1. IP Lookup              6. Cookie Inspector")
        print(WHITE + " 2. Reverse DNS            7. Robots.txt Scraper")
        print(WHITE + " 3. Port Scanner           8. Tech Stack Detector")
        print(WHITE + " 4. Ping Target            9. HTTP Headers")
        print(WHITE + " 5. DNS Lookup            10. Link Unshortener")
        print(WHITE + "")
        print(WHITE + " [UTILITIES]")
        print(WHITE + " 11. Base64 Encoder/Decoder")
        print(WHITE + " 12. Hash Generator")
        print(WHITE + " 13. Password Generator")
        print(WHITE + " 14. Subdomain Scanner")
        print(WHITE + "\n [0]  Exit\n")
        
        try:
            choice = input(PROMPT).strip()
            if choice == "0":
                print(WHITE + "\n[*] Powering down... Goodbye.")
                sys.exit()
            if choice == "1": ip_lookup()
            elif choice == "2": reverse_dns()
            elif choice == "3": port_scanner()
            elif choice == "4": ping_target()
            elif choice == "5": dns_lookup()
            elif choice == "6": cookie_inspector()
            elif choice == "7": robots_txt()
            elif choice == "8": tech_detect()
            elif choice == "9": header_grabber()
            elif choice == "10": link_unshortener()
            elif choice == "11": base64_tool()
            elif choice == "12": hash_generator()
            elif choice == "13": password_generator()
            elif choice == "14": subdomain_scanner()
            else:
                print(RED + "\n[-] Invalid option.")
                time.sleep(1)
                continue
        except KeyboardInterrupt:
            print(RED + "\n\n[!] Operation Cancelled. Returning to menu...")
            time.sleep(1)
        except Exception as e:
            print(RED + f"\n\n[!] Unknown Error: {e}")
            time.sleep(1)
            
        input(DIM_WHITE + "\nPress Enter to return to the menu...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(WHITE + "\n\n[*] Exiting...")
        sys.exit()
