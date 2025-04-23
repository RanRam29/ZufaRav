import { useEffect, useState } from "react";
import axios from "../axiosInstance";
import { useNavigate, Link } from "react-router-dom";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";
import markerIcon2x from "leaflet/dist/images/marker-icon-2x.png";
import markerIcon from "leaflet/dist/images/marker-icon.png";
import markerShadow from "leaflet/dist/images/marker-shadow.png";
import "leaflet/dist/leaflet.css";

const confirmSound = new Audio("https://assets.mixkit.co/sfx/preview/mixkit-correct-answer-tone-2870.mp3");
const notifySound = new Audio("https://assets.mixkit.co/sfx/preview/mixkit-alert-bells-echo-765.wav");

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});

function formatMinutesSince(dateString) {
  const created = new Date(dateString);
  const now = new Date();
  const diffInMinutes = Math.floor((now - created) / 60000);

  if (diffInMinutes < 1) return "פחות מדקה";
  if (diffInMinutes === 1) return "דקה אחת";
  if (diffInMinutes < 60) return `${diffInMinutes} דקות`;

  const diffInHours = Math.floor(diffInMinutes / 60);
  if (diffInHours < 24) return `${diffInHours} שעות`;

  const diffInDays = Math.floor(diffInHours / 24);
  return `${diffInDays} ימים`;
}

export default function Dashboard() {
  const [events, setEvents] = useState([]);
  const [userLocation, setUserLocation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [filterConfirmed, setFilterConfirmed] = useState("all");
  const [showLogoutPopup, setShowLogoutPopup] = useState(false);
  const navigate = useNavigate();

  const token = localStorage.getItem("token");
  const username = localStorage.getItem("username");
  const role = localStorage.getItem("role");

  useEffect(() => {
    if (!token) navigate("/login");
  }, [token]);

  useEffect(() => {
    fetchEvents();

    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setUserLocation({
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          });
        },
        (error) => {
          console.error("שגיאה בקבלת מיקום המשתמש", error);
        },
        { enableHighAccuracy: true }
      );
    }

    const interval = setInterval(async () => {
      const res = await axios.get("/events/list");
      const now = new Date();
      const recent = res.data.filter((event) => {
        const created = new Date(event.datetime);
        const diff = (now - created) / (1000 * 60);
        return diff < 2;
      });
      if (recent.length > 0) {
        notifySound.play();
        alert("📣 אירוע חדש נוצר במערכת!");
      }
    }, 10000);

    return () => clearInterval(interval);
  }, []);

  const fetchEvents = async () => {
    try {
      const res = await axios.get("/events/list");
      setEvents(res.data);
    } catch {
      alert("שגיאה בטעינת האירועים");
    }
    setLoading(false);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    localStorage.removeItem("role");
    setShowLogoutPopup(true);
    setTimeout(() => {
      setShowLogoutPopup(false);
      navigate("/login", { replace: true });
    }, 1500);
  };

  const handleJoinEvent = async (title) => {
    try {
      await axios.post(`/events/confirm/${title}`);
      confirmSound.play();
      fetchEvents();
    } catch (err) {
      alert("שגיאה באישור ההגעה");
    }
  };

  const handleDeleteById = async (id) => {
    const confirmed = window.confirm("האם אתה בטוח שברצונך למחוק את האירוע? פעולה זו אינה הפיכה.");
    if (!confirmed) return;
    try {
      await axios.delete(`/events/delete/by_id/${id}`);
      setEvents((prev) => prev.filter((e) => e.id !== id));
    } catch {
      alert("שגיאה במחיקה");
    }
  };

  const getDistanceFromLatLonInKm = (lat1, lon1, lat2, lon2) => {
    const R = 6371;
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
      Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
  };

  const severityColor = (event) => {
    const createdTime = new Date(event.datetime);
    const now = new Date();
    const minutesAgo = Math.floor((now - createdTime) / 60000);
    const hoursAgo = Math.floor(minutesAgo / 60);
    const daysAgo = Math.floor(hoursAgo / 24);
    const distance = event.distance || 0;

    if (distance <= 100) return "bg-green-100 border-green-500 text-green-700";
    if (daysAgo >= 1) return "bg-gray-200 border-gray-500 text-gray-700";
    if (hoursAgo >= 1) return "bg-yellow-200 border-yellow-500 text-yellow-700";
    if (minutesAgo >= 15) return "bg-orange-200 border-orange-500 text-orange-700";
    if (minutesAgo >= 5) return "bg-red-200 border-red-500 text-red-700 animate-pulse";
    return "bg-white border-gray-300 text-gray-900";
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6 text-right">
      {showLogoutPopup && (
        <div className="fixed top-4 left-1/2 transform -translate-x-1/2 bg-white shadow-lg border px-6 py-2 rounded-xl z-50 animate-fade">
          ✅ נותקת מהמערכת
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {events.map((event) => (
          <div key={event.id} className={`p-4 rounded-xl shadow ${severityColor(event)}`}>
            <h3 className="text-xl font-bold">{event.title}</h3>
            <p>מדווח: {event.reporter}</p>
            <p>סטטוס: {event.confirmed ? "✅ מאושר" : "⏳ בהמתנה"}</p>
            <p>בהמתנה: {formatMinutesSince(event.datetime)}</p>
            <p>משתתפים: {event.people_count || 0}</p>
            {userLocation && event.lat && event.lng && (() => {
              const dist = getDistanceFromLatLonInKm(
                userLocation.lat,
                userLocation.lng,
                event.lat,
                event.lng
              );
              const icon = "📍";
              let color = "text-red-600";
              if (dist < 0.5) color = "text-green-700";
              else if (dist < 2) color = "text-orange-600";
              return (
                <p className={color}>
                  {dist < 1
                    ? `${icon} מרחק: ${Math.round(dist * 1000)} מטר`
                    : `${icon} מרחק: ${dist.toFixed(2)} ק"מ`}
                </p>
              );
            })()}
            <div className="flex gap-2 mt-2">
              <button onClick={() => handleJoinEvent(event.title)} className="bg-purple-600 hover:bg-purple-700 text-white px-2 rounded">
                מאשר הגעה
              </button>
              <button onClick={() => handleDeleteById(event.id)} className="bg-red-500 text-white px-2 rounded">
                מחק
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}