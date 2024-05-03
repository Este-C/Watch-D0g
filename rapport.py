from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Image
import json
import os
import sys

# Get the IP address and Hostname from command line arguments
Ip = sys.argv[1]
if len(sys.argv) >= 3:
    Hostname = sys.argv[2]
else:
    Hostname = ""

# Delete old scan results file if it exists
def delete_file_if_exists(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)
        print(f"Deleted existing file at {file_path}")

# Define the path for the PDF file in the ./result directory
report_file_path = f"./assets/scan_results{Hostname}.pdf"
delete_file_if_exists(report_file_path)

# Load data from the JSON file
with open('./database.json') as f:
    data = json.load(f)

# Create a PDF document with a letter size
doc = SimpleDocTemplate(report_file_path, pagesize=letter)

# Define the PDF content
elements = []

# Add Hostname and IP address to the top left of the first page
header = f"Target - IP: {Ip} / Hostname: {Hostname}"
header_paragraph = Paragraph(header, getSampleStyleSheet()["BodyText"])
elements.append(header_paragraph)

# Add a title paragraph
title = "Scan Results"
title_paragraph = Paragraph(title, getSampleStyleSheet()["Title"])
elements.append(title_paragraph)

# Add a spacer
elements.append(Spacer(1, 12 * mm))

# Add favicon to the top right corner
favicon_path = "./assets/collected/favicon.png"
if os.path.exists(favicon_path):
    with open(favicon_path, 'rb') as f:
        img = ImageReader(f)
        img_width, img_height = img.getSize()
        aspect_ratio = img_width / img_height
        favicon_width = 20  # Adjust this value as needed
        favicon_height = favicon_width / aspect_ratio
        elements.append(Image(favicon_path, width=favicon_width, height=favicon_height, hAlign='RIGHT'))

# Add the NMAP scan results
nmap_scan_results_paragraph = Paragraph("NMAP Scan Results:", getSampleStyleSheet()["Heading2"])
elements.append(nmap_scan_results_paragraph)

if 'NMAP SCAN' in data:
    nmap_scan_results = data["NMAP SCAN"]["Scan_Results"]
    if nmap_scan_results:
        for result in nmap_scan_results:
            port = result["port"]
            service = result["service"]
            version = result["version"]
            nmap_scan_result_paragraph = Paragraph(f"Port: {port}, Service: {service}, Version: {version}", getSampleStyleSheet()["BodyText"])
            elements.append(nmap_scan_result_paragraph)
    else:
        nmap_scan_result_paragraph = Paragraph("No NMAP scan results found.", getSampleStyleSheet()["BodyText"])
        elements.append(nmap_scan_result_paragraph)
else:
    nmap_scan_result_paragraph = Paragraph("No NMAP scan results found.", getSampleStyleSheet()["BodyText"])
    elements.append(nmap_scan_result_paragraph)

# Add CVEs and exploit information
cve_exploit_paragraph = Paragraph("CVEs and Exploits:", getSampleStyleSheet()["Heading2"])
elements.append(cve_exploit_paragraph)

if 'CVE_EXPLOIT' in data:
    cve_exploit_results = data["CVE_EXPLOIT"]
    if cve_exploit_results:
        for result in cve_exploit_results:
            cve_list = ", ".join(result["cvelist"]) if result.get("cvelist") else "N/A"
            exploit_link = result.get("href", "N/A")
            exploit_description = result.get("description", "N/A")
            published_date = result.get("published", "N/A")
            cvss_score = result.get("cvss", {}).get("score", "N/A")
            cve_exploit_info = f"Published Date: {published_date}<br/>CVEs: {cve_list}<br/>CVSS Score: {cvss_score}<br/>Exploit Description: {exploit_description}<br/>Exploit Link: {exploit_link}"
            cve_exploit_info_paragraph = Paragraph(cve_exploit_info, getSampleStyleSheet()["BodyText"])
            elements.append(cve_exploit_info_paragraph)
            # Add a little space between each CVE exploit
            elements.append(Spacer(1, 6))
    else:
        cve_exploit_info_paragraph = Paragraph("No CVEs and exploits found.", getSampleStyleSheet()["BodyText"])
        elements.append(cve_exploit_info_paragraph)
else:
    cve_exploit_info_paragraph = Paragraph("No CVEs and exploits found.", getSampleStyleSheet()["BodyText"])
    elements.append(cve_exploit_info_paragraph)

# Add a spacer
elements.append(Spacer(1, 12 * mm))

# Add the DIRECTORY scan results
directory_scan_results_paragraph = Paragraph("DIRECTORY Scan Results:", getSampleStyleSheet()["Heading2"])
elements.append(directory_scan_results_paragraph)
if 'DIRECTORY SCAN' in data:
    directory_scan_results = data["DIRECTORY SCAN"]["Scan_Results"]
    if isinstance(directory_scan_results, list):
        for result in directory_scan_results:
            directory_scan_result_paragraph = Paragraph(f"Directory: {result['Directory']}, Status: {result['Status']}, Size: {result['Size']}, Redirect: {result['Redirect']}", getSampleStyleSheet()["BodyText"])
            elements.append(directory_scan_result_paragraph)
    elif isinstance(directory_scan_results, str):
        directory_scan_results = directory_scan_results.split('\n')
        for result in directory_scan_results:
            directory_scan_result_paragraph = Paragraph(result, getSampleStyleSheet()["BodyText"])
            elements.append(directory_scan_result_paragraph)
else:
    directory_scan_result_paragraph = Paragraph("No DIRECTORY scan results found.", getSampleStyleSheet()["BodyText"])
    elements.append(directory_scan_result_paragraph)

# Add a spacer
elements.append(Spacer(1, 12 * mm))

# Add the NIKTO scan results
nikto_scan_results_paragraph = Paragraph("NIKTO Scan Results:", getSampleStyleSheet()["Heading2"])
elements.append(nikto_scan_results_paragraph)
nikto_scan_results = json.loads(data["NIKTO SCAN"]["Scan_Results"])
for result in nikto_scan_results["vulnerabilities"]:
    nikto_scan_result_paragraph = Paragraph(f"ID: {result['id']}, Method: {result['method']}, URL: {result['url']}, Message: {result['msg']}", getSampleStyleSheet()["BodyText"])
    elements.append(nikto_scan_result_paragraph)

# Add the SSH Brute Force results
ssh_bruteforce_paragraph = Paragraph("SSH Bruteforce Results:", getSampleStyleSheet()["Heading2"])
elements.append(ssh_bruteforce_paragraph)
if 'SSH Bruteforce' in data:
    ssh_bruteforce_results = data["SSH Bruteforce"]["Results"]
    if ssh_bruteforce_results:
        for result in ssh_bruteforce_results:
            ssh_bruteforce_result_paragraph = Paragraph(f"IP: {result['IP']}, Username: {result['Username']}, Password: {result['Password']}", getSampleStyleSheet()["BodyText"])
            elements.append(ssh_bruteforce_result_paragraph)
    else:
        ssh_bruteforce_result_paragraph = Paragraph("No SSH Brute Force results found.", getSampleStyleSheet()["BodyText"])
        elements.append(ssh_bruteforce_result_paragraph)
else:
    ssh_bruteforce_result_paragraph = Paragraph("No SSH Brute Force results found.", getSampleStyleSheet()["BodyText"])
    elements.append(ssh_bruteforce_result_paragraph)

# Add a second-degree title for "Information gathered"
information_gathered_title = Paragraph("Information Gathered:", getSampleStyleSheet()["Heading3"])
elements.append(information_gathered_title)

# Load and add data from gather.txt
gather_data_path = "./assets/collected/gather.txt"
if os.path.exists(gather_data_path):
    with open(gather_data_path, 'r') as gather_file:
        gather_data_lines = gather_file.readlines()
    
    formatted_gather_data = ""
    for line in gather_data_lines:
        if line.strip():
            formatted_gather_data += line.rstrip(";") + "<br/><br/>"
    
    # Add formatted data to the report
    gather_data_paragraph = Paragraph(formatted_gather_data, getSampleStyleSheet()["BodyText"])
    elements.append(gather_data_paragraph)
else:
    no_gather_data_paragraph = Paragraph("No gathered information data found.", getSampleStyleSheet()["BodyText"])
    elements.append(no_gather_data_paragraph)

# Build the PDF document
doc.build(elements)

# flushing data
def delete_file_if_exists(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)
        print(f"Deleted existing file at {file_path}")

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

def empty_file(file_path):
    try:
        # Open the file in write mode, which clears its contents
        with open(file_path, 'w') as file:
            pass  # Pass does nothing, so it just opens and immediately closes the file
        print("File emptied successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

file_path = "./database.json"
empty_file(file_path)

print("")
print("Report generated ! ")
print("")