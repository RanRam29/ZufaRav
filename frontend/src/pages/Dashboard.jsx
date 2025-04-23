
import React, { useEffect, useState } from 'react';
import axios from '../axiosInstance';
import { useNavigate, Link } from 'react-router-dom';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import L from 'leaflet';
import "leaflet/dist/leaflet.css";

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png'
});

const confirmSound = new Audio("https://assets.mixkit.co/sfx/preview/mixkit-correct-answer-tone-2870.mp3");
const notifySound = new Audio("https://assets.mixkit.co/sfx/preview/mixkit-alert-bells-echo-765.wav");

export default function Dashboard() {
  const [events, setEvents] = useState([]);
  const [userLocation, setUserLocation] = useState(null);
  const [filterConfirmed, setFilterConfirmed] = useState("all");
  const [showLogoutPopup, setShowLogoutPopup] = useState(false);
  const navigate = useNavigate();

  const token = localStorage.getItem("token");
  const username = localStorage.getItem("username");
  const role = localStorage.getItem("role");

  useEffect(() => {
    if (!token) navigate("/login");
  }, [token]);

  const getDistance = (lat1, lon1, lat2, lon2) => {
    const R = 6371e3;
    const φ1 = lat1 * Math.PI / 180;
    const φ2 = lat2 * Math.PI / 180;
    const Δφ = (lat2 - lat1) * Math.PI / 180;
    const Δλ = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(Δφ/2)**2 + Math.cos(φ1)*Math.cos(φ2)*Math.sin(Δλ/2)**2;
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return R * c;
  };

  const getTimeLabel = (datetime) => {
    const created = new Date(datetime);
    const now = new Date();
    const diffMin = Math.floor((now - created) / 60000);
    if (diffMin < 1) return "פחות מדקה";
    if (diffMin < 60) return `${diffMin} דקות`;
    const hours = Math.floor(diffMin / 60);
    if (hours < 24) return `${hours} שעות`;
    return `${Math.floor(hours / 24)} ימים`;
  };

  const getBackgroundClass = (event) => {
    const created = new Date(event.datetime);
    const now = new Date();
    const minutesAgo = Math.floor((now - created) / 60000);
    if (minutesAgo < 5) return "bg-green-100 animate-pulse";
    if (minutesAgo < 15) return "bg-yellow-100";
    if (minutesAgo < 60) return "bg-orange-100";
    return "bg-gray-100";
  };

  const getTextColorByDistance = (dist) => {
    if (dist < 100) return "text-green-700";
    if (dist < 1000) return "text-orange-600";
    return "text-red-600";
  };

  const fetchEvents = async () => {
    try {
      const res = await axios.get("/events/list");
      setEvents(res.data);
    } catch {
      alert("שגיאה בטעינת האירועים");
    }
  };

  useEffect(() => {
    fetchEvents();
    const watchId = navigator.geolocation?.watchPosition(
      (pos) => {
        const coords = { lat: pos.coords.latitude, lng: pos.coords.longitude };
        setUserLocation(coords);
        axios.post("/tracking/update", { username, ...coords });
      },
      (err) => console.error("שגיאת GPS", err),
      { enableHighAccuracy: true }
    );
    const interval = setInterval(async () => {
      const res = await axios.get("/events/list");
      const now = new Date();
      const recent = res.data.filter(e => {
  const created = new Date(e.datetime);
  const diff = (now - created) / 60000;
  return diff < 2 && !e.confirmed;
});
      if (recent.length) {
        notifySound.play();
        alert("📣 אירוע חדש נוצר במערכת!");
      }
    }, 10000);
    return () => {
      navigator.geolocation.clearWatch(watchId);
      clearInterval(interval);
    };
  }, []);

  const handleLogout = () => {
    localStorage.clear();
    setShowLogoutPopup(true);
    setTimeout(() => {
      setShowLogoutPopup(false);
      navigate("/login");
    }, 1500);
  };

  const confirmEvent = async (title) => {
    try {
      await axios.post(`/events/confirm/${title}`);
      confirmSound.play();
      fetchEvents();
    } catch {
      alert("שגיאה באישור הגעה");
    }
  };

  const deleteEvent = async (id) => {
    if (!confirm("האם אתה בטוח שברצונך למחוק את האירוע?")) return;
    try {
      await axios.delete(`/events/delete/by_id/${id}`);
      fetchEvents();
    } catch {
      alert("שגיאה במחיקה");
    }
  };

  const filteredEvents = events.filter(e => {
    if (filterConfirmed === "confirmed") return e.confirmed;
    if (filterConfirmed === "pending") return !e.confirmed;
    return true;
  });

  return (
    <div className="min-h-screen bg-gray-100 p-6 text-right">
      <div className="flex justify-between items-center mb-4">
        <div>
          <h2 className="text-2xl font-bold">דשבורד אירועים</h2>
          <p>משתמש: <b>{username}</b> | תפקיד: <b>{role}</b></p>
        </div>
        <div className="flex gap-2">
          {(role === "admin" || role === "hamal") && (
            <Link to="/create-event" className="bg-green-600 text-white px-4 py-2 rounded-xl">צור אירוע חדש</Link>
          )}
          <button onClick={() => navigate("/movement")} className="bg-blue-600 text-white px-4 py-2 rounded-xl">דשבורד תנועה</button>
          <button onClick={handleLogout} className="bg-gray-500 text-white px-4 py-2 rounded-xl">התנתק</button>
                  <button onClick={() => navigate("/reports")} className="bg-gray-700 text-white px-4 py-2 rounded-xl">ארכיון</button>
        </div>
      </div>

      <div className="flex gap-2 mb-4 justify-end">
        <button onClick={() => setFilterConfirmed("all")} className="bg-gray-300 px-3 py-1 rounded">הצג הכל</button>
        <button onClick={() => setFilterConfirmed("confirmed")} className="bg-green-300 px-3 py-1 rounded">מאושרים</button>
        <button onClick={() => setFilterConfirmed("pending")} className="bg-yellow-300 px-3 py-1 rounded">בהמתנה</button>
      </div>

      {showLogoutPopup && (
        <div className="fixed top-4 left-1/2 transform -translate-x-1/2 bg-white border px-6 py-2 rounded-xl z-50 shadow-lg animate-fade">✅ נותקת מהמערכת</div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        {filteredEvents.map((event) => {
          const dist = userLocation && event.lat && event.lng
            ? getDistance(userLocation.lat, userLocation.lng, event.lat, event.lng)
            : null;
          const distText = dist < 1000
            ? `${Math.round(dist)} מטר`
            : `${(dist / 1000).toFixed(2)} ק״מ`;
          return (
            <div key={event.title} className={`rounded-xl p-4 shadow ${getBackgroundClass(event)}`}>
              <h3 className="text-lg font-bold">{event.title}</h3>
              <p>מדווח: {event.reporter}</p>
              <p>סטטוס: {event.confirmed ? "✅ מאושר" : "⏳ ממתין"}</p>
              <p>בהמתנה: {getTimeLabel(event.datetime)}</p>
              <p>משתתפים: {event.people_count || 0}</p>
              {dist && (
                <p className={`${getTextColorByDistance(dist)}`}>📍 מרחק: {distText}</p>
              )}
              <div className="flex gap-2 mt-2">
                {!event.confirmed && (
                  <button onClick={() => confirmEvent(event.title)} className="bg-purple-600 text-white px-2 rounded">מאשר הגעה</button>
                )}
                <button onClick={() => deleteEvent(event.id)} className="bg-red-500 text-white px-2 rounded">מחק</button>
              </div>
            </div>
          );
        })}
      </div>

      <MapContainer center={[31.8, 35.2]} zoom={8} scrollWheelZoom={false} style={{ height: '400px', width: '100%' }}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        {userLocation && (
          <>
            <Marker position={[userLocation.lat, userLocation.lng]}>
              <Popup>המיקום שלך</Popup>
            </Marker>
            <Circle center={[userLocation.lat, userLocation.lng]} radius={100} pathOptions={{ color: 'blue' }} />
          </>
        )}
        {events.map((e, i) => (
          e.lat && e.lng && (
            <Marker key={i} position={[e.lat, e.lng]}>
              <Popup>
                <strong>{e.title}</strong><br />
                {e.address}<br />
                מדווח: {e.reporter}<br />
                סטטוס: {e.confirmed ? '✅' : '⏳'}
              </Popup>
            </Marker>
          )
        ))}
      </MapContainer>
    </div>
  );
}
