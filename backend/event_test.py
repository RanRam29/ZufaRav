import requests

API_BASE = "https://zufarav.onrender.com"

headers = {
    "Content-Type": "application/json",
    "X-User": "admin1"
}

def test_create_event():
    print("🚀 Creating event...")
    response = requests.post(f"{API_BASE}/events/create", json={
        "title": "בדיקת מערכת",
        "location": "תל אביב",
        "reporter": "admin1",
        "severity": "HIGH",
        "people_required": 2,
        "datetime": "2025-04-23T10:00:00",
        "lat": 32.0853,
        "lng": 34.7818
    }, headers=headers)
    print(response.json())

def test_list_events():
    print("📋 Listing events...")
    response = requests.get(f"{API_BASE}/events/list")
    events = response.json()
    print(events)
    return events

def test_confirm_event(title):
    print(f"✅ Confirming event: {title}")
    response = requests.post(f"{API_BASE}/events/confirm/{title}", headers=headers)
    print(response.json())

def test_join_event(event_id):
    print(f"👥 Joining event {event_id}...")
    response = requests.post(f"{API_BASE}/events/join", json={
        "event_id": event_id,
        "username": "rav1"
    }, headers=headers)
    print(response.json())

def test_delete_event_by_id(event_id):
    print(f"🗑 Deleting event {event_id}...")
    response = requests.delete(f"{API_BASE}/events/delete/by_id/{event_id}", headers=headers)
    print(response.json())

def test_get_archive():
    print("📦 Getting archive...")
    response = requests.get(f"{API_BASE}/events/archive", headers=headers)
    print(response.json())

if __name__ == "__main__":
    test_create_event()
    events = test_list_events()
    if events:
        event = events[-1]
        test_confirm_event(event["title"])
        test_join_event(event["id"])
        test_delete_event_by_id(event["id"])
        test_get_archive()
