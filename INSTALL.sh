#!/bin/bash

# Install required packages
echo "Installing required packages..."
sudo apt-get update
sudo apt-get install -y python3 nikto nmap gobuster dnsrecon hydra wget sqlmap sshpass ftp

# Install Python libraries
echo "Installing Python libraries..."
pip install -r requirements.txt

echo "Installation complete!"

echo "Launching the Toolbox !"
python3 ./main.py