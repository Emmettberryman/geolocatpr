#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from ip_utils import get_ip_info

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org')
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching IP address: {e}")
        return None

def print_ip_details(ip_address):
    api_response = get_ip_info(ip_address)

    if api_response:
        longitude = api_response.get('longitude')
        latitude = api_response.get('latitude')
        country = api_response.get('country_name')
        city = api_response.get('city_name')
        zipcode = api_response.get('zip_code')

        if all([longitude, latitude, country, city, zipcode]):
            print(f"IP Address: {ip_address}")
            print(f"Longitude: {longitude}")
            print(f"Latitude: {latitude}")
            print(f"Country: {country}")
            print(f"City: {city}")
            print(f"Zip Code: {zipcode}")
        else:
            print("Some location details are missing in the API response.")
    else:
        print("Failed to retrieve IP information.")

def main():
    ip_address = get_public_ip()
    if ip_address:
        print(f"Your public IP address is: {ip_address}")
        print_ip_details(ip_address)
    else:
        print("Unable to proceed without a valid IP address.")

if __name__ == "__main__":
    main()