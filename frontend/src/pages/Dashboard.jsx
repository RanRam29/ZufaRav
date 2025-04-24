
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
    if (!token) {
      window.location.href = "/login";  // ✅ רידיירקט קשיח
    }
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
    const interval = setInterval(() => {
      fetchEvents();
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
      window.location.href = "/login";  // ✅ תיקון רידיירקט
    }, 1000);
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
    <div>/* content omitted for brevity */</div>
  );
}
