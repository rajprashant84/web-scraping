import tldextract
import requests
from bs4 import BeautifulSoup
import json

def extract_websites(email_addresses):
    websites = []
    email_lines = email_addresses.split('\n')

    for email_line in email_lines:
        domain = tldextract.extract(email_line.split('@')[1]).domain
        if domain:
            website_url = "http://www." + domain + "." + tldextract.extract(email_line.split('@')[1]).suffix
            websites.append(website_url)

    return websites

def get_company_info_from_website(website_url):
    try:
        response = requests.get(website_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Replace the selectors below with the appropriate HTML elements for company name and address
        company_name = soup.select_one('title').get_text().strip()

        address_element = soup.select_one('address')  # Replace 'address' with the appropriate selector for address
        address = address_element.get_text().strip() if address_element else None

        email_element = soup.select_one('a[href^="mailto:"]')
        email = email_element.get('href').replace('mailto:', '').strip() if email_element else None

        return company_name, address, email

    except Exception as e:
        return None, None, None

def read_email_addresses_from_file(file_path):
    with open(file_path, 'r') as file:
        email_addresses = file.read()

    return email_addresses

# Specify the path to the file containing email addresses
file_path = 'email_addresses.txt'

# Read email addresses from the file
email_addresses = read_email_addresses_from_file(file_path)

# Extract websites
results = extract_websites(email_addresses)

# Create a dictionary to store the company details with website URLs as keys
company_details = {}
for website in results:
    company_name, address, email = get_company_info_from_website(website)
    if company_name:
        company_details[website] = {
            "company_name": company_name,
            "address": address,
            "email": email
        }

# Convert the company details dictionary to JSON and print
output = {"websites": company_details}
print(json.dumps(output, indent=2))
