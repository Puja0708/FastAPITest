import requests

def get_location_from_ip(ip_address: str) -> dict:
    response = requests.get(f"https://ipapi.co/{ip_address}/json/")
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Location lookup failed"}
