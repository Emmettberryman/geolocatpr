#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from typing import Union

def check_location_in_csv(longitude: Union[float, str], latitude: Union[float, str], csv_file: str, tolerance: float = 1e-6) -> bool:
    """Checks if the given longitude and latitude exist in the CSV file and prints the offense description."""
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file}' not found.")
        return False

    longitude = float(longitude)
    latitude = float(latitude)

    for index, row in df.iterrows():
        csv_longitude = float(row['longitude'])
        csv_latitude = float(row['latitude'])
        if abs(csv_longitude - longitude) < tolerance and abs(csv_latitude - latitude) < tolerance:
            print(f"Location found in CSV at row {index}")
            print(f"Offense Description: {row['OFFENSE_DESCRIPTION']}")
            return True

    print("Location not found in CSV.")
    return False