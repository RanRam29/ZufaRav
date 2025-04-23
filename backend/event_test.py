import requests
from datetime import datetime
import random

API = "https://zufarav.onrender.com"  # שנה לפי הצורך אם אתה מריץ ב-Render

username = f"testuser{random.randint(1000,9999)}"
password = "12345678"

def register_user():
    data = {
        "username": username,
        "password": password,
        "rank": "טוראי",
        "role": "admin",  # או hamal/rav
        "id_number": f"{random.randint(100000000, 999999999)}",
        "phone_number": f"05{random.randint(00000000,99999999)}"
    }
    res = requests.post(f"{API}/auth/register", json=data)
    print("✅ Register:", res.status_code, res.text)

def login_user():
    res = requests.post(f"{API}/auth/login", json={
        "username": username,
        "password": password
    })
    print("✅ Login:", res.status_code)
    return res.json()["access_token"]

def create_event(token):
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "title": "בדיקת אירוע",
        "location": "תל אביב",
        "reporter": username,
        "severity": "HIGH",
        "people_required": 3,
        "datetime": datetime.utcnow().isoformat(),
        "lat": 32.0853,
        "lng": 34.7818
    }
    res = requests.post(f"{API}/events/create", json=data, headers=headers)
    print("✅ Create Event:", res.status_code, res.text)

def list_events():
    res = requests.get(f"{API}/events/list")
    print("📄 All Events:")
    for e in res.json():
        print("-", e["title"], "by", e["reporter"], "| Confirmed:", e["confirmed"])

if __name__ == "__main__":
    print("📦 Starting test flow...")
    register_user()
    token = login_user()
    create_event(token)
    list_events()
