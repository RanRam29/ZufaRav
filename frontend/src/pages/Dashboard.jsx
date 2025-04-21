import { useEffect, useState } from "react";
import axios from "../axiosInstance";
import { useNavigate, Link } from "react-router-dom";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";

export default function Dashboard() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchEvents();

    const interval = setInterval(async () => {
      const res = await axios.get("/events/list");
      const now = new Date();
      const recent = res.data.filter(event => {
        const created = new Date(event.datetime);
        const diff = (now - created) / (1000 * 60); // דקות
        return diff < 2;
      });
      if (recent.length > 0) {
        alert("📣 אירוע חדש נוצר במערכת!");
      }
    }, 10000);

    return () => clearInterval(interval);
  }, []);

  const fetchEvents = async () => {
    try {
      const res = await axios.get("/events/list");
      setEvents(res.data);
    } catch (err) {
      alert("שגיאה בטעינת האירועים");
    }
    setLoading(false);
  };

  const handleDeleteById = async (id) => {
    if (!confirm("למחוק אירוע לפי ID?")) return;
    try {
      await axios.delete(`/events/delete/by_id/${id}`);
      setEvents((prev) => prev.filter((e) => e.id !== id));
    } catch {
      alert("שגיאה במחיקה");
    }
  };

  const handleDeleteByTitle = async (title) => {
    if (!confirm("למחוק אירוע לפי כותרת?")) return;
    try {
      await axios.delete(`/events/delete/${title}`);
      setEvents((prev) => prev.filter((e) => e.title !== title));
    } catch {
      alert("שגיאה במחיקה");
    }
  };

  const updateCountById = async (id, delta) => {
    const event = events.find((e) => e.id === id);
    const newCount = Math.max((event.people_count || 0) + delta, 0);
    try {
      await axios.patch(`/events/update_people_count/by_id`, {
        id,
        new_count: newCount,
      });
      setEvents((prev) =>
        prev.map((e) => (e.id === id ? { ...e, people_count: newCount } : e))
      );
    } catch {
      alert("שגיאה בעדכון");
    }
  };

  const handleDeleteByReporter = async (reporter) => {
    if (!confirm(`למחוק את כל האירועים של ${reporter}?`)) return;
    try {
      await axios.delete(`/events/delete/by_reporter/${reporter}`);
      setEvents((prev) => prev.filter((e) => e.reporter !== reporter));
    } catch {
      alert("שגיאה במחיקת כל האירועים של המשתמש");
    }
  };

  const handleJoinEvent = async (eventId) => {
    const username = localStorage.getItem("username");
    try {
      await axios.post("/events/join", {
        event_id: eventId,
        username,
      });
      alert("אישרת הגעה לאירוע בהצלחה!");
    } catch {
      alert("שגיאה באישור הגעה");
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6 text-right">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-2 mb-6">
        <h1 className="text-2xl font-bold text-gray-800">דשבורד אירועים</h1>
        <div className="flex gap-2">
          <Link
            to="/create-event"
            className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-xl"
          >
            צור אירוע חדש
          </Link>
          <button
            onClick={() => navigate("/movement")}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-xl"
          >
            דשבורד תנועה
          </button>
        </div>
      </div>

      {loading ? (
        <p>טוען אירועים...</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {events.map((event) => (
            <div key={event.id} className="bg-white p-4 rounded-xl shadow">
              <h3 className="text-xl font-bold text-blue-800">{event.title}</h3>
              <p>מיקום: {event.location}</p>
              <p>מדווח: {event.reporter}</p>
              <p>משתתפים: {event.people_count || 0}</p>

              <div className="flex gap-2 mt-2">
                <button
                  onClick={() => updateCountById(event.id, 1)}
                  className="bg-green-600 text-white px-2 rounded"
                >
                  +
                </button>
                <button
                  onClick={() => updateCountById(event.id, -1)}
                  className="bg-yellow-500 text-white px-2 rounded"
                >
                  -
                </button>
                <button
                  onClick={() => handleJoinEvent(event.id)}
                  className="bg-purple-600 hover:bg-purple-700 text-white px-2 rounded"
                >
                  מאשר הגעה
                </button>
              </div>

              <div className="flex gap-2 mt-2 text-sm">
                <button
                  onClick={() => handleDeleteByTitle(event.title)}
                  className="text-blue-500 underline"
                >
                  מחיקה לפי כותרת
                </button>
                <button
                  onClick={() => handleDeleteByReporter(event.reporter)}
                  className="text-red-500 underline"
                >
                  מחיקת כל האירועים של המשתמש
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
