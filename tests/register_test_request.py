import requests

url = "https://zufarav.onrender.com/auth/register"

payload = {
    "username": "בדיקה",
    "password": "1234",
    "rank": "רס"ר",
    "role": "user",
    "id_number": "9876543",
    "phone_number": "050-9876543",
    "full_name": "בודק המערכת",
    "email": "test@example.com"
}

try:
    r = requests.post(url, json=payload)
    print("Status:", r.status_code)
    print("Response:", r.json())
except Exception as e:
    print("❌ Request failed:", e)
