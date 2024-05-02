import threading
import time
import sys
import subprocess
import nmap
import json
import os
import vulners
from colorama import Fore, Style, Back

Ip = sys.argv[1]
Hostname = sys.argv[2]

scan_result = []

stop_threads = False

# Scan funtion
def gather_info(ip):
    global scan_result
    try:
        nm = nmap.PortScanner()
        nm.scan(ip, arguments='-sV -T4')

# Scan parsing results
        scan_result = []
        for host in nm.all_hosts():
            if nm[host].state() == 'up':
                for proto in nm[host].all_protocols():
                    ports = nm[host][proto].keys()
                    for port in ports:
                        service = nm[host][proto][port]['name']
                        version = nm[host][proto][port]['version']
                        scan_result.append({'port': port, 'service': service, 'version': version})

        data = {}
        if os.path.isfile('database.json'):
            with open('database.json') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {'NMAP SCAN': {'Scan_Results': []}}
        else:
            data = {'NMAP SCAN': {'Scan_Results': []}}

        if 'NMAP SCAN' not in data:
            data['NMAP SCAN'] = {'Scan_Results': []}
        data['NMAP SCAN']['Scan_Results'].extend(scan_result)

# Save the scan results to the database 
        with open('database.json', 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print("An error occurred in the thread:", e)

# Loading animation
def loading_animation():
    animations = ['\\', '|', '/', '-']
    idx = 0
    while not stop_threads:
        print('\rScanning... ' + animations[idx % len(animations)], end='', flush=True)
        idx += 1
        time.sleep(0.1)

# Searches for exploits using vulners.com API
def search_exploits(scan_result):
    # vulners.com API key
    vulners_api = vulners.VulnersApi('1B98SBNPOEDH9N238Q4M058MQDMCSY7VO7A6KZG3QHYFATN58WGXVM9JC2FVQ35H')
    exploit_list = []
    for result in scan_result:
        service = result['service']
        version = result['version']
        query = f"{service} {version}"
        results = vulners_api.get_software_vulnerabilities(service, version)
        exploit_list += results.get('exploit', [])
    return exploit_list

loading_thread = threading.Thread(target=loading_animation)
loading_thread.start()

gather_info(Ip)
exploit_list = search_exploits(scan_result)

stop_threads = True
loading_thread.join()

# print results
print("\n")
print(Fore.YELLOW + '-----------------------------------------------------------------------' + Style.RESET_ALL)
print(Fore.GREEN + "Scan Results:" + Style.RESET_ALL)
print(scan_result)
print("")
print(Fore.YELLOW + '-----------------------------------------------------------------------' + Style.RESET_ALL)

# Update database with CVE and exploit list
data = {}
if os.path.isfile('database.json'):
    with open('database.json') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = {'NMAP SCAN': {'Scan_Results': []}}
else:
    data = {'NMAP SCAN': {'Scan_Results': []}}

if 'CVE_EXPLOIT' not in data:
    data['CVE_EXPLOIT'] = []

data['CVE_EXPLOIT'].extend(exploit_list)

with open('database.json', 'w') as f:
    json.dump(data, f, indent=4)

# call next page
subprocess.call(['python3', 'dir.py', Ip, Hostname])
