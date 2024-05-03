import threading
import time
import sys
import subprocess
import json
import os
import socket
from colorama import Fore, Style, Back

# Récupération des informations du menu main
Hostname = sys.argv[1]
Ip = sys.argv[2]

# Variable globale pour stocker le résultat de la numérisation
dns_result = []

done = False

# Dns Recon bruteforce
def dns_recon(Hostname):
    global dns_result, done

    if not Hostname:
        print(Back.RED + "Hostname variable is empty. Going to SCAN IP." + Style.RESET_ALL)
        subprocess.call(['python3', 'scan.py', Ip, Hostname])
        return

    # Get ip from domain
    def get_ip_from_domain(Hostname):
        try:
            ip_address = socket.gethostbyname(Hostname)
            return ip_address
        except socket.gaierror:
            return None

    ipFound = get_ip_from_domain(Hostname)
    if ipFound is not None:
        print(Back.GREEN + f'The {Hostname} IP Address is {ipFound}' + Style.RESET_ALL)
    else:
        print(Fore.RED + f'Failed to get the IP address for {Hostname}' + Style.RESET_ALL)
        subprocess.call(['python3', 'main.py'])
        return

    # Starting DNS Recon
    print(Fore.YELLOW + f"Performing DNS recon on {Hostname}..." + Style.RESET_ALL)
    try:
        dns_process = subprocess.Popen(['dnsrecon', '-d', Hostname, '-t', 'brt', '-D', './assets/wordlist/subdomains.txt'],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError as e:
        print(Fore.RED + f"Error: {e} Please ensure dnsrecon is installed and accessible." + Style.RESET_ALL)
        subprocess.call(['python3', 'scan.py', ipFound, Hostname])
        return

    loading_thread = threading.Thread(target=loading_animation)
    loading_thread.start()

    dns_output, dns_error = dns_process.communicate()

    done = True
    loading_thread.join()

    # if error going to ip scan
    if dns_process.returncode != 0:
        print(f"Error: {dns_error.decode()}")
        print(Fore.RED + "DNS recon failed. Going to scan IP." + Style.RESET_ALL)
        subprocess.call(['python3', 'scan.py', ipFound, Hostname])
        return

    # print output
    print(Fore.LIGHTGREEN_EX + "DNS recon completed successfully." + Style.RESET_ALL)
    print("")
    print(Fore.YELLOW + '-----------------------------------------------------------------------' + Style.RESET_ALL)
    print(dns_output.decode())

    # Load the JSON data from the file
    if os.path.isfile('database.json'):
        with open('database.json') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {'DNS SCAN': {'Scan_Results': []}}
    else:
        data = {'DNS SCAN': {'Scan_Results': []}}

    # Save the directory scan's information to the JSON file
    data['DNS SCAN'] = {'Scan_Results': dns_output.decode()}
    with open('database.json', 'w') as f:
        json.dump(data, f, indent=4)

    # récupère SVG de la cible pour le rapport
    subprocess.call(['wget', f'https://favicone.com/{Hostname}?s=256', '-O', './assets/collected/favicon.png'])
    if os.path.exists('./assets/collected/favicon.png'):
        print("SVG image collected successfully.")
        print(Fore.YELLOW + '-----------------------------------------------------------------------' + Style.RESET_ALL)

    else:
        print("Failed to collect SVG image.")
        print(Fore.YELLOW + '-----------------------------------------------------------------------' + Style.RESET_ALL)


    subprocess.call(['python3', 'scan.py', ipFound, Hostname])

def loading_animation():
    animations = ['\\', '|', '/', '-']
    idx = 0
    while not done:
        print('\rPerforming DNS recon... ' + animations[idx % len(animations)], end='', flush=True)
        idx += 1
        time.sleep(0.1)

dns_recon(Hostname)