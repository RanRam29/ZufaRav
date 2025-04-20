
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png'
});

export default function Dashboard() {
  const [events, setEvents] = useState([]);
  const [newEvent, setNewEvent] = useState({ title: '', location: '', reporter: 'hamal' });

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
      await axios.post('http://localhost:8000/events/create', newEvent);
      setNewEvent({ title: '', location: '', reporter: 'hamal' });
      fetchEvents();
    } catch {
      alert('שגיאה ביצירת אירוע');
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

  useEffect(() => {
    fetchEvents();
  }, []);

  return (
    <div style={{ direction: 'rtl', padding: '2rem' }}>
      <h2>דשבורד עם מפה חיה</h2>

      <div style={{ marginBottom: '2rem' }}>
        <h4>צור אירוע חדש</h4>
        <input
          placeholder="כותרת"
          value={newEvent.title}
          onChange={e => setNewEvent({ ...newEvent, title: e.target.value })}
        />
        <br />
        <input
          placeholder="מיקום"
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
        {events.map((e, i) => (
          <Marker key={i} position={[31.8 + i * 0.01, 35.2 + i * 0.01]}>
            <Popup>
              <div>
                <strong>{e.title}</strong><br />
                {e.location}<br />
                סטטוס: {e.confirmed ? '✅ מאושר' : '⏳ ממתין'}
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>

      <h4>רשימת אירועים:</h4>
      {events.map((e, i) => (
        <div key={i} style={{ border: '1px solid gray', padding: '1rem', marginBottom: '1rem' }}>
          <strong>{e.title}</strong> - {e.location}
          <br />
          מדווח: {e.reporter}
          <br />
          סטטוס: {e.confirmed ? '✅ מאושר' : '⏳ ממתין'}
          <br />
          {!e.confirmed && (
            <button onClick={() => confirmEvent(e.title)}>מאשר הגעה</button>
          )}
        </div>
      ))}
    </div>
  );
}
