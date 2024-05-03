import subprocess
import sys
import os
import json
import threading
import time
from colorama import Fore, Style, Back

# Retrieving information from the previous page
Ip = sys.argv[1]
Hostname = sys.argv[2]

# delete file if exist because it block the process
def delete_file_if_exists(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)
        print(Back.YELLOW + f"Deleted existing file at {file_path}" + Style.RESET_ALL)

def loading_animation():
    animations = ['\\', '|', '/', '-']
    idx = 0
    while not done:
        print('\rNikto Scan in progress... ' + animations[idx % len(animations)], end='', flush=True)
        idx += 1
        time.sleep(0.1)

# Nikto scan function
def nikto_scan(ip):
    global done
    done = False
    loading_thread = threading.Thread(target=loading_animation)
    

    report_file_path = "./assets/collected/report.json"
    delete_file_if_exists(report_file_path)

    loading_thread.start()
    # Run the Nikto scan
    command = ['nikto', '-Display', '34EP', '-o', report_file_path, '-Format', 'json', '-Tuning', '12bde', '-host', ip]
    result = subprocess.run(command, capture_output=True, text=True)
    done = True
    loading_thread.join()

    # Print the Nikto scan report
    if os.path.isfile(report_file_path):
        print("")
        print(Fore.GREEN + "Nikto Scan Report:" +Style.RESET_ALL)
        print("")
        with open(report_file_path, 'r') as report_file:
            report_content = report_file.read()
            print(report_content)
        print(Fore.YELLOW + '-----------------------------------------------------------------------' + Style.RESET_ALL)
    

        # Load the JSON data from the file
        if os.path.isfile('database.json'):
            with open('database.json') as f:
                data = json.load(f)
        else:
            data = {'NIKTO SCAN': {'Scan_Results': []}}

        # Save the Nikto scan information to the JSON file
        data['NIKTO SCAN'] = {'Scan_Results': report_content}
        with open('database.json', 'w') as f:
            json.dump(data, f, indent=4)
        
    else:
        print("")
        print(Fore.YELLOW + '-----------------------------------------------------------------------' + Style.RESET_ALL)
        print("Nikto Scan Error:")
        print(result.stderr)


nikto_scan(Ip)
subprocess.call(['python3', 'attack_menu.py', Ip, Hostname])
