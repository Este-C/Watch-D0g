import subprocess
import sys
import os
from colorama import Fore, Style, Back

# Récupération des informations de la page précédente
Ip = sys.argv[1]
Hostname = sys.argv[2]

# Clear the screen
def clear_screen():
    os.system('clear')

def show_menu(ip):
    #clear_screen()
    print(Fore.YELLOW + """

*****************************************************************************
 __          __     _       _           _____   ___
 \ \        / /___ | |     | |         |  __ \ / _ \\
  \ \  /\  / / __ \| |_ ___| |__ ______| |  | | | | | __ _
   \ \/  \/ / / _` | __/ __| '_ \______| |  | | | | |/ _` |
    \  /\  / | (_| | || (__| | | |     | |__| | |_| | (_| |
     \/  \/ \ \__,_|\__\___|_| |_|     |_____/ \___/ \__, |
             \____/                                   __/ /
                                                     |___/
                                                   By : 6sco
**************************************************___________****************

""")
    print()
    print('-----------------------------------------------------------------------' + Style.RESET_ALL)
    print()
    print("Attack Menu:")
    print(Fore.CYAN + "1"+ Style.RESET_ALL + " - SQL Attack")
    print(Fore.CYAN + "2"+ Style.RESET_ALL + " - SSH Attack")
    print(Fore.YELLOW + "3"+ Style.RESET_ALL + " - Web Login Attack (Experimental)")
    print(Fore.YELLOW + "4"+ Style.RESET_ALL + " - Automated Attack (Experimental)")
    print(Fore.CYAN + "5"+ Style.RESET_ALL + " - Generate report and flushing data")
    print(Fore.RED + "6"+ Style.RESET_ALL + " - Clean DATA and Exit")
    while True:
        choice = input("Select your choice: ")
        if choice == '1':
            subprocess.call(['python3', 'Auto_sqlmap.py', ip, Hostname])
            break
        elif choice == '2':
            subprocess.call(['python3', 'exploit_SSH.py', ip, Hostname])
            break
        elif choice == '3':
            subprocess.call(['python3', 'exploit_login.py', ip])
            break
        elif choice == '4':
            subprocess.call(['python3', 'auto_exploit.py', ip])
            break
        elif choice == '5':
            print("")
            print(Fore.YELLOW + "Report will be generated in result directory..." + Style.RESET_ALL)
            subprocess.call(['python3', 'rapport.py', ip, Hostname])
            break
        elif choice == '6':
            nmap_data = "./assets/collected/nmap_scan.txt"
            sqlmap_data = "./assets/collected/sqlmap_data.json"
            gather_data = "./assets/collected/gather.txt"
            favicon = "./assets/collected/favicon.png"
            nikto_data = "./assets/collected/report.json"
            delete_file_if_exists(nmap_data)
            delete_file_if_exists(sqlmap_data)
            delete_file_if_exists(gather_data)
            delete_file_if_exists(favicon)
            delete_file_if_exists(nikto_data)
            empty_file(file_path)
            print(Fore.RED + "Everything is clean, Bye !" + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)

# flushing data function
def delete_file_if_exists(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)
        print(f"Deleted existing file at {file_path}")

# empty file function
def empty_file(file_path):
    try:
        # Open the file in write mode, which clears its contents
        with open(file_path, 'w') as file:
            pass  # Pass does nothing, so it just opens and immediately closes the file
        print("File emptied successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

file_path = "./database.json"

show_menu(Ip)