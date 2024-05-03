import re
import subprocess
from colorama import Fore, Style, Back

def check_password_strength(password):
    # Check if password length is at least 8 characters
    if len(password) < 8:
        return "Weak", "Password length should be at least 8 characters"
    
    # Check if password contains at least one uppercase letter, one lowercase letter, one digit, and one special character
    if not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(r'\d', password) or not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return "Medium", "Password should contain at least one uppercase letter, one lowercase letter, one digit, and one special character"
    
    # Check if password is not a common password
    common_passwords = ["password", "123456", "qwerty", "abc123", "AZERTY", "azerty", "Pa$$w0rd", "QWERTY", "admin", "root", "toor", "apple"] # Add more common passwords if needed
    if password.lower() in common_passwords:
        return "Medium", "Password is too common"
    
    return "Strong", "Password is strong"

def main():
    while True:
        print("")
        print(Fore.CYAN + "1"+ Style.RESET_ALL + "  Check Password Strength")
        print(Fore.RED + "2"+ Style.RESET_ALL + "  Exit")
        print("")
        choice = input("Enter your choice: ")

        if choice == "1":
            password = input("Enter your password: ")
            strength, vulnerability = check_password_strength(password)
            print("Password Strength:", strength)
            print("Vulnerability:", vulnerability)
        elif choice == "2":
            print("Returning to main menu ...")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

main()
subprocess.call(['python3', 'main.py'])