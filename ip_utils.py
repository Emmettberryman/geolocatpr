#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from typing import Dict, Optional

def get_ip_info(ip_address: str) -> Optional[Dict]:
    """Fetches and returns IP address information from the API."""
    payload = {'key': '65E02FE2DF28CEEEE4324C5EC6283EB7', 'ip': ip_address, 'format': 'json'}
    try:
        api_result = requests.get('https://api.ip2location.io/', params=payload)
        api_result.raise_for_status()  # Raise an exception for HTTP errors
        api_response = api_result.json()
        return api_response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching IP information: {e}")
        return None