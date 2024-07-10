#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ip_utils import get_ip_info
from csv_utils import check_location_in_csv

def main():
    ip_address = input('Please enter an IP address: ')
    api_response = get_ip_info(ip_address)

    if api_response:
        longitude = api_response.get('longitude')
        latitude = api_response.get('latitude')

        if longitude is not None and latitude is not None:
            print(f"Longitude: {longitude}, Latitude: {latitude}")
            csv_file = "csvfile.csv"
            location_found = check_location_in_csv(longitude, latitude, csv_file)
        else:
            print("Longitude and/or Latitude not found in API response.")

if __name__ == "__main__":
    main()