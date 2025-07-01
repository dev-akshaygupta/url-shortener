from uuid import uuid4
import requests

def generate_short_code():
    return uuid4().hex[:6]

def get_country_from_ip(ip: str) -> str:
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        return data.get("countryCode", "XX")
    except Exception:
        return "XX"