import React, { useEffect, useState, useRef } from 'react';
import axios from '../axiosInstance';
import { useNavigate } from 'react-router-dom';
import TopBar from '../components/TopBar';
import FilterBar from '../components/FilterBar';
import LogoutPopup from '../components/LogoutPopup';
import EventsGrid from '../components/EventsGrid';
import MapSection from '../components/MapSection';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const confirmSound = new Audio("/notification.mp3");
const notifySound = new Audio("/notification.mp3");

export default function Dashboard() {
  const [events, setEvents] = useState([]);
  const [userLocation, setUserLocation] = useState(null);
  const [filterConfirmed, setFilterConfirmed] = useState("all");
  const [showLogoutPopup, setShowLogoutPopup] = useState(false);
  const [newEventIds, setNewEventIds] = useState([]);  // חדש - לשמור מזהי אירועים חדשים
  const navigate = useNavigate();
  const notifiedEvents = useRef(new Set());

  const token = localStorage.getItem("token");
  const username = localStorage.getItem("username");
  const role = localStorage.getItem("role");

  useEffect(() => {
    if (!token) window.location.href = "/login";
  }, [token]);

  useEffect(() => {
    const socket = new WebSocket("wss://zufarav.onrender.com/ws/events");

    socket.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.type === "new_event" && !notifiedEvents.current.has(msg.data.id)) {
        notifiedEvents.current.add(msg.data.id);
        // עדכון רשימת האירועים החדשים
        setNewEventIds((prev) => [...prev, msg.data.id]);

        // ניגון הצליל
        notifySound.play().catch((err) => {
          console.error("Error playing notification sound:", err);
        });

        // נוטיפיקציה לדפדפן
        if (Notification.permission === "granted") {
          new Notification("📢 אירוע חדש", {
            body: msg.data.title,
            icon: "/favicon.ico", // תוכל להחליף לאייקון שלך אם יש
          });
        }

        // הצגת Toast
        toast.info(`📣 אירוע חדש: ${msg.data.title}`, {
          position: "bottom-right",
          autoClose: 5000,
        });

        // עדכון האירועים
        setEvents((prev) => [...prev, msg.data]);
      }
    };

    return () => socket.close();
  }, []);

  const getDistance = (lat1, lon1, lat2, lon2) => {
    const R = 6371e3;
    const φ1 = lat1 * Math.PI / 180;
    const φ2 = lat2 * Math.PI / 180;
    const Δφ = (lat2 - lat1) * Math.PI / 180;
    const Δλ = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(Δφ / 2) ** 2 + Math.cos(φ1) * Math.cos(φ2) * Math.sin(Δλ / 2) ** 2;
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
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
    let lastSentCoords = null;

    const geoWatchId = navigator.geolocation?.watchPosition(
      (pos) => {
        const coords = { lat: pos.coords.latitude, lng: pos.coords.longitude };
        const moved = !lastSentCoords ||
                      Math.abs(coords.lat - lastSentCoords.lat) > 0.0001 ||
                      Math.abs(coords.lng - lastSentCoords.lng) > 0.0001;

        if (moved) {
          lastSentCoords = coords;
          setUserLocation(coords);
          axios.post("/tracking/update", {
            username,
            ...coords,
            timestamp: new Date().toISOString(),
          });
        }
      },
      (err) => console.error("שגיאת GPS", err),
      { enableHighAccuracy: true }
    );

    const interval = setInterval(fetchEvents, 10000);

    return () => {
      navigator.geolocation.clearWatch(geoWatchId);
      clearInterval(interval);
    };
  }, []);

  const handleLogout = () => {
    localStorage.clear();
    setShowLogoutPopup(true);
    setTimeout(() => {
      setShowLogoutPopup(false);
      window.location.href = "/login";
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
    <div className="min-h-screen bg-gray-100 p-6 text-right">
      <ToastContainer />
      <TopBar username={username} role={role} navigate={navigate} handleLogout={handleLogout} />
      <FilterBar setFilterConfirmed={setFilterConfirmed} />
      <LogoutPopup show={showLogoutPopup} />
      <EventsGrid
        events={filteredEvents}
        userLocation={userLocation}
        getDistance={getDistance}
        getTextColorByDistance={getTextColorByDistance}
        getBackgroundClass={getBackgroundClass}
        getTimeLabel={getTimeLabel}
        confirmEvent={confirmEvent}
        deleteEvent={deleteEvent}
        newEventIds={newEventIds}  // הוסף את ה־newEventIds
      />
      <MapSection userLocation={userLocation} events={events} newEventIds={newEventIds} />
    </div>
  );
}
