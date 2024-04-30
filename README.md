# W@tch-D0g Toolbox

## Prerequisites

This code should be run on a Linux distribution such as Debian (tested on Debian-Kali Linux).

---

### Required Packages

Make sure the following packages are installed:

- Python 3
- Nikto
- Nmap
- Gobuster
- DNSRecon
- Hydra
- Wget
- Sqlmap

If you encounter issues with Hydra's SSH brute force, run the following command:

    $ kali-tweaks -h 

select '**hardening**' then select '**ssh client**'

---

## Quick Installation

Run this command :

    $ chmod +x ./INSTALL.sh
    $ ./INSTALL.sh

It should install all the library and package needed. 

---

## Quick modification

go to **assets/wordlist/**
there you can add your wordlist.

**/!\ : rename the file as follow : ***

> - directory.txt   --> wordlist of subdirectories
> - rockyou.txt     --> wordlist of password
> - subdomains.txt  --> wordlist of subdomains
> - usernames.txt   --> wordlist of usernames
