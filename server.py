import http.server
import socketserver
import json
import requests
from urllib.parse import urlparse, parse_qs

# Function to get public IP (from your previous code)
def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org')
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching IP address: {e}")
        return None

# Function to get IP info (from your previous code)
def get_ip_info(ip_address):
    payload = {'key': '65E02FE2DF28CEEEE4324C5EC6283EB7', 'ip': ip_address, 'format': 'json'}
    try:
        api_result = requests.get('https://api.ip2location.io/', params=payload)
        api_result.raise_for_status()
        return api_result.json()
    except requests.RequestException as e:
        print(f"Error fetching IP information: {e}")
        return None

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/api/ip-info'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            ip_address = get_public_ip()
            if ip_address:
                api_response = get_ip_info(ip_address)
                if api_response:
                    response = {
                        'ip_address': ip_address,
                        'longitude': api_response.get('longitude', 'N/A'),
                        'latitude': api_response.get('latitude', 'N/A'),
                        'country': api_response.get('country_name', 'N/A'),
                        'city': api_response.get('city_name', 'N/A'),
                        'zipcode': api_response.get('zip_code', 'N/A')
                    }
                else:
                    response = {'error': 'Failed to retrieve IP information'}
            else:
                response = {'error': 'Unable to get IP address'}
            
            self.wfile.write(json.dumps(response).encode())
        else:
            super().do_GET()

PORT = 8000

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()