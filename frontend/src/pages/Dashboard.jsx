import { useEffect, useState } from "react";
import axios from "../axiosInstance";
import { useNavigate } from "react-router-dom";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";

export default function Dashboard() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchEvents();
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

  return (
    <div className="min-h-screen bg-gray-100 p-6 text-right">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-800">דשבורד אירועים</h1>
        <button
          onClick={() => navigate("/movement")}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-xl"
        >
          מעבר לדשבורד תנועה
        </button>
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
                  onClick={() => handleDeleteById(event.id)}
                  className="bg-red-600 text-white px-2 rounded ml-auto"
                >
                  מחיקה לפי ID
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
