#!/usr/bin/python3
import requests
import json
import os
from dotenv import load_dotenv 
from datetime import datetime

def log_message(message):
  print(f"{datetime.now().isoformat()} - {message}")

load_dotenv()
API_KEY = os.getenv('DNS_PORKBUN_KEY')
SECRET_KEY = os.getenv('DNS_PORKBUN_SECRET')
TTL = os.getenv('DNS_TTL', 300)
NAMES = os.getenv('DNS_RECORDS').split(',')
DOMAIN = os.getenv('DNS_DOMAIN')

def edit_dns_record(api_key, secret_key, domain, id, record_type, name, content, ttl):
  url = f'https://api.porkbun.com/api/json/v3/dns/edit/{domain}/{id}'
  headers = {'Content-Type': 'application/json'}
  payload = {
    'apikey': api_key,
    'secretapikey': secret_key,
    'type': record_type,
    'name': name,
    'content': content,
    'ttl': ttl
  }
  try:
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    log_message(f"Successfully edited DNS record for {name}.{domain}")
    return response.json()
  except requests.exceptions.RequestException as e:
    log_message(f"Error editing DNS record: {e}")
    exit(1)

def get_dns_record(api_key, secret_key, domain, record_type, name):
  url = f'https://api.porkbun.com/api/json/v3/dns/retrieveByNameType/{domain}/{record_type}/{name}'
  headers = {'Content-Type': 'application/json'}
  payload = {
    'apikey': api_key,
    'secretapikey': secret_key
  }
  try:
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    log_message(f"Successfully retrieved DNS record for {name}.{domain}")
    return response.json()
  except requests.exceptions.RequestException as e:
    log_message(f"Error retrieving DNS record: {e}")
    exit(1)

def create_dns_record(api_key, secret_key, domain, record_type, name, content, ttl):
  url = f'https://api.porkbun.com/api/json/v3/dns/create/{domain}'
  headers = {'Content-Type': 'application/json'}
  payload = {
    'apikey': api_key,
    'secretapikey': secret_key,
    'type': record_type,
    'name': name,
    'content': content,
    'ttl': ttl
  }
  try:
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    log_message(f"Successfully created DNS record for {name}.{domain}")
    return response.json()
  except requests.exceptions.RequestException as e:
    log_message(f"Error creating DNS record: {e}")
    exit(1)

def get_public_ip():
  url = 'https://v4.ident.me/'
  try:
    response = requests.get(url)
    response.raise_for_status()
    ip = response.text
    log_message(f"Successfully retrieved public IP: {ip}")
    return ip
  except requests.exceptions.RequestException as e:
    log_message(f"Error getting public IP: {e}")
    exit(1)

def main():
  current_public_ip = get_public_ip()
  record_type = 'A'
  content = current_public_ip

  for name in NAMES: 
    response = get_dns_record(API_KEY, SECRET_KEY, DOMAIN, record_type, name)

    if 'records' in response and response['records']:
      if current_public_ip == response['records'][0]['content']:
        log_message(f'{name} - IP address has not changed')
      else:
        log_message(f'{name} - IP address has changed')
        id = response['records'][0]['id']
        response = edit_dns_record(API_KEY, SECRET_KEY, DOMAIN, id, record_type, name, content, TTL)
        log_message(str(response))
    else:
      log_message(f'{name} - No DNS record found')
      log_message(f'{name} - Creating new DNS record')
      response = create_dns_record(API_KEY, SECRET_KEY, DOMAIN, record_type, name, content, TTL)
      log_message(str(response))

if __name__ == '__main__':
  main()
