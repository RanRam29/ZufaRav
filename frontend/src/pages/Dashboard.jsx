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

// ✅ תיקון Leaflet למחט קלאסית
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});

function formatMinutesSince(dateString) {
  const created = new Date(dateString);
  const now = new Date();
  const diff = Math.floor((now - created) / 60000);
  if (diff < 1) return "פחות מדקה";
  if (diff === 1) return "דקה אחת";
  return `${diff} דקות`;
}

export default function Dashboard() {
  const [events, setEvents] = useState([]);
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

  const filteredEvents = events.filter((event) => {
    if (filterConfirmed === "all") return true;
    if (filterConfirmed === "confirmed") return event.confirmed;
    if (filterConfirmed === "pending") return !event.confirmed;
    return true;
  });

  const severityColor = (event) => {
    const severity = event.severity;
    const createdTime = new Date(event.datetime);
    const now = new Date();
    const minutesAgo = Math.floor((now - createdTime) / 60000);
    const distance = event.distance || 0;

    if (distance <= 100) return "text-green-700 font-bold";
    if (minutesAgo < 5) return severity === "HIGH" ? "text-red-600 animate-pulse" : "text-yellow-600";
    if (minutesAgo < 15) return "text-orange-600";
    return "text-gray-500";
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6 text-right">
      {showLogoutPopup && (
        <div className="fixed top-4 left-1/2 transform -translate-x-1/2 bg-white shadow-lg border px-6 py-2 rounded-xl z-50 animate-fade">
          ✅ נותקת מהמערכת
        </div>
      )}

      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-2 mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">דשבורד אירועים</h1>
          <p className="text-sm text-gray-600">
            משתמש: <b>{username}</b> | תפקיד: <b>{role}</b>
          </p>
        </div>
        <div className="flex gap-2 flex-wrap">
          {(role === "admin" || role === "hamal") && (
            <Link
              to="/create-event"
              className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-xl"
            >
              צור אירוע חדש
            </Link>
          )}
          <button
            onClick={() => navigate("/movement")}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-xl"
          >
            דשבורד תנועה
          </button>
          <button
            onClick={handleLogout}
            className="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded-xl"
          >
            התנתק
          </button>
        </div>
      </div>

      <div className="flex justify-end gap-2 mb-4">
        <button
          onClick={() => setFilterConfirmed("all")}
          className="bg-gray-300 hover:bg-gray-400 text-gray-800 px-3 py-1 rounded"
        >
          הצג הכל
        </button>
        <button
          onClick={() => setFilterConfirmed("confirmed")}
          className="bg-green-300 hover:bg-green-400 text-gray-800 px-3 py-1 rounded"
        >
          מאושרים
        </button>
        <button
          onClick={() => setFilterConfirmed("pending")}
          className="bg-yellow-300 hover:bg-yellow-400 text-gray-800 px-3 py-1 rounded"
        >
          בהמתנה
        </button>
      </div>

      {loading ? (
        <p>טוען אירועים...</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {filteredEvents.map((event) => (
            <div key={event.id} className="bg-white p-4 rounded-xl shadow transition-transform duration-300 hover:scale-105">
              <h3 className={`text-xl font-bold ${severityColor(event)}`}>
                {event.title}
              </h3>
              <p>מיקום: {event.location}</p>
              <p>מדווח: {event.reporter}</p>
              <p>רמת חומרה: {event.severity}</p>
              <p>סטטוס: {event.confirmed ? "✅ מאושר" : "⏳ בהמתנה"}</p>
              <p>בהמתנה: {formatMinutesSince(event.datetime)}</p>
              <p>משתתפים: {event.people_count || 0}</p>

              <div className="flex gap-2 mt-2">
                <button
                  onClick={() => handleJoinEvent(event.title)}
                  className="bg-purple-600 hover:bg-purple-700 text-white px-2 rounded"
                >
                  מאשר הגעה
                </button>
                <button
                  onClick={() => handleDeleteById(event.id)}
                  className="bg-red-500 text-white px-2 rounded"
                >
                  מחק
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="mt-8">
        <MapContainer center={[31.0461, 34.8516]} zoom={7} style={{ height: "400px" }}>
          <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
          {events.map((event) => (
            <Marker key={event.id} position={[event.lat, event.lng]}>
              <Popup>{event.title}</Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>
    </div>
  );
}
