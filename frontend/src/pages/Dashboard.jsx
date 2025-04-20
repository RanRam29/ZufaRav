import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png'
});

export default function Dashboard() {
  const username = localStorage.getItem("username") || "לא מזוהה";
  const [events, setEvents] = useState([]);
  const [newEvent, setNewEvent] = useState({ title: '', location: '', reporter: username });
  const [userLocation, setUserLocation] = useState(null);

  const fetchEvents = async () => {
    try {
      const res = await axios.get('http://localhost:8000/events/list');
      setEvents(res.data);
    } catch {
      alert('שגיאה בשליפת אירועים');
    }
  };

  const createEvent = async () => {
    try {
      const geoRes = await axios.get('https://nominatim.openstreetmap.org/search', {
        params: {
          q: newEvent.location,
          format: 'json',
          limit: 1
        }
      });

      if (!geoRes.data.length) {
        alert("כתובת לא נמצאה במפה 😕");
        return;
      }

      const { lat, lon } = geoRes.data[0];

      const reverseRes = await axios.get('https://nominatim.openstreetmap.org/reverse', {
        params: {
          lat,
          lon,
          format: 'json'
        }
      });

      const address = reverseRes.data.display_name || "כתובת לא זמינה";

      const fullEvent = {
        ...newEvent,
        lat: parseFloat(lat),
        lng: parseFloat(lon),
        address
      };

      await axios.post('http://localhost:8000/events/create', fullEvent);
      setNewEvent({ title: '', location: '', reporter: username });
      fetchEvents();
    } catch (err) {
      alert('שגיאה ביצירת אירוע');
      console.error(err);
    }
  };

  const confirmEvent = async (title) => {
    try {
      await axios.post(`http://localhost:8000/events/confirm/${title}`);
      fetchEvents();
    } catch {
      alert("שגיאה באישור האירוע");
    }
  };

  const getDistanceFromLatLonInMeters = (lat1, lon1, lat2, lon2) => {
    const R = 6371e3; // רדיוס כדור הארץ במטרים
    const φ1 = lat1 * Math.PI / 180;
    const φ2 = lat2 * Math.PI / 180;
    const Δφ = (lat2 - lat1) * Math.PI / 180;
    const Δλ = (lon2 - lon1) * Math.PI / 180;

    const a = Math.sin(Δφ/2) * Math.sin(Δφ/2) +
              Math.cos(φ1) * Math.cos(φ2) *
              Math.sin(Δλ/2) * Math.sin(Δλ/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));

    return R * c; // במטרים
  };

  useEffect(() => {
    fetchEvents();
    if (navigator.geolocation) {
      const watchId = navigator.geolocation.watchPosition(
        position => {
          const coords = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
          };
          setUserLocation(coords);
          sendLiveLocation(coords.lat, coords.lng); // 👈 כאן הקריאה
        },
        error => {
          console.error("שגיאה בקבלת מיקום:", error);
        },
        { enableHighAccuracy: true, maximumAge: 5000, timeout: 10000 }
      );
  
      return () => navigator.geolocation.clearWatch(watchId);
    }
  }, []);
  
  
  const sendLiveLocation = (lat, lng) => {
    axios.post("http://localhost:8000/tracking/update", {
      username,
      lat,
      lng
    }).catch(err => {
      console.error("שגיאה בשליחת מיקום לשרת:", err);
    });
  };
  

  return (
    <div style={{ direction: 'rtl', padding: '2rem' }}>
      <h2>דשבורד עם מפה חיה</h2>
      <h4>משתמש מחובר: {username}</h4>

      <div style={{ marginBottom: '2rem' }}>
        <h4>צור אירוע חדש</h4>
        <input
          placeholder="כותרת"
          value={newEvent.title}
          onChange={e => setNewEvent({ ...newEvent, title: e.target.value })}
        />
        <br />
        <input
          placeholder="כתובת מדויקת"
          value={newEvent.location}
          onChange={e => setNewEvent({ ...newEvent, location: e.target.value })}
        />
        <br />
        <button onClick={createEvent}>צור אירוע</button>
      </div>

      <MapContainer
        center={[31.8, 35.2]}
        zoom={8}
        scrollWheelZoom={false}
        style={{ height: '400px', width: '100%', marginBottom: '2rem' }}
        maxBounds={[[29.45, 34.25], [33.3, 35.9]]}
        maxBoundsViscosity={1.0}
      >
        <TileLayer
          attribution='&copy; <a href="https://openstreetmap.org">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {userLocation && (
          <>
            <Marker position={[userLocation.lat, userLocation.lng]}>
              <Popup>המיקום שלך</Popup>
            </Marker>
            <Circle
              center={[userLocation.lat, userLocation.lng]}
              radius={100}
              pathOptions={{ color: 'blue', fillOpacity: 0.1 }}
            />
          </>
        )}

        {events.map((e, i) => {
          const distance = userLocation ? getDistanceFromLatLonInMeters(userLocation.lat, userLocation.lng, e.lat, e.lng) : null;
          const onSite = distance !== null && distance <= 100;

          return e.lat && e.lng && (
            <Marker key={i} position={[e.lat, e.lng]}>
              <Popup>
                <div>
                  <strong>{e.title}</strong><br />
                  {e.address || e.location}<br />
                  מדווח: {e.reporter}<br />
                  סטטוס: {e.confirmed ? '✅ מאושר' : '⏳ ממתין'}<br />
                  {userLocation && (
                    <span>
                      מרחק: {Math.round(distance)} מטר<br />
                      {onSite ? "🟢 אתה בזירה" : "🔴 אתה רחוק מהזירה"}
                    </span>
                  )}
                </div>
              </Popup>
            </Marker>
          );
        })}
      </MapContainer>

      <h4>רשימת אירועים:</h4>
      {events.map((e, i) => {
        const distance = userLocation ? getDistanceFromLatLonInMeters(userLocation.lat, userLocation.lng, e.lat, e.lng) : null;
        const onSite = distance !== null && distance <= 100;

        return (
          <div key={i} style={{ border: '1px solid gray', padding: '1rem', marginBottom: '1rem' }}>
            <strong>{e.title}</strong> - {e.address || e.location}
            <br />
            מדווח: {e.reporter}
            <br />
            סטטוס: {e.confirmed ? '✅ מאושר' : '⏳ ממתין'}
            <br />
            {userLocation && (
              <div>
                מרחק: {Math.round(distance)} מטר<br />
                {onSite ? "🟢 אתה בזירה" : "🔴 אתה רחוק מהזירה"}
              </div>
            )}
            {!e.confirmed && (
              <button onClick={() => confirmEvent(e.title)}>מאשר הגעה</button>
            )}
          </div>
        );
      })}
    </div>
  );
}
