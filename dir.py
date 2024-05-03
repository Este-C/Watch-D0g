import subprocess
import sys
import json
import os
import re
import threading
import time
from colorama import Fore, Style, Back

# Récupération des informations de la page précédente
Ip = sys.argv[1]
Hostname = sys.argv[2]

def loading_animation():
    animations = ['\\', '|', '/', '-']
    idx = 0
    while not done:
        print('\rScanning directories... ' + animations[idx % len(animations)], end='', flush=True)
        idx += 1
        time.sleep(0.1)

# Dir scan function
def dir_scan(ip):
    global done
    done = False
    loading_thread = threading.Thread(target=loading_animation)
    loading_thread.start()

    # Gobuster command
    command = ['gobuster', 'dir', '-u', f'http://{ip}/', '-w', './assets/wordlist/directory.txt', '-q', '--no-error', '--no-color']
    result = subprocess.run(command, capture_output=True, text=True)

    # Load the JSON data from the file
    if os.path.isfile('database.json'):
        with open('database.json') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {'DIRECTORY SCAN': {'Scan_Results': []}}
    else:
        data = {'DIRECTORY SCAN': {'Scan_Results': []}}

    # Clean up the result.stdout
    cleaned_stdout = re.sub(r'(\n\n\u001b\[2K|\n\u001b\[2K)', '', result.stdout)

    # Save the directory scan's information to the JSON file
    data['DIRECTORY SCAN'] = {'Scan_Results': cleaned_stdout}
    with open('database.json', 'w') as f:
        json.dump(data, f, indent=4)

    done = True
    loading_thread.join()

    # Display the result
    if result.returncode == 0:
        print("")
        print(Fore.GREEN + "Directory Scan Results:" + Style.RESET_ALL)
        print(result.stdout)
        print("")
        print(Fore.YELLOW + '-----------------------------------------------------------------------' + Style.RESET_ALL)
    else:
        print("")
        print("Gobuster Scan Error:")
        print(result.stderr)
        print("")
        print(Fore.YELLOW + '-----------------------------------------------------------------------' + Style.RESET_ALL)

dir_scan(Ip)
subprocess.call(['python3', 'websearch.py', Ip, Hostname])
