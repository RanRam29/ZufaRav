import { useEffect, useState } from "react";
import axios from "axios";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { useNavigate } from "react-router-dom";

export default function Dashboard() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const fetchEvents = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/events/list`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      setEvents(res.data);
    } catch (err) {
      setError("אירעה שגיאה בטעינת האירועים");
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchEvents();
  }, []);

  const handleDelete = async (id) => {
    if (!confirm("האם למחוק את האירוע?")) return;
    try {
      await axios.delete(`${import.meta.env.VITE_API_BASE_URL}/events/${id}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      setEvents((prev) => prev.filter((e) => e.id !== id));
    } catch {
      alert("שגיאה במחיקה");
    }
  };

  const updateCount = async (id, delta) => {
    const event = events.find((e) => e.id === id);
    const newCount = Math.max((event.people_count || 0) + delta, 0);
    try {
      await axios.patch(`${import.meta.env.VITE_API_BASE_URL}/events/update_people_count`, {
        id,
        new_count: newCount,
      }, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      setEvents((prev) =>
        prev.map((e) => (e.id === id ? { ...e, people_count: newCount } : e))
      );
    } catch {
      alert("שגיאה בעדכון כמות");
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

      {loading && <p className="text-center text-gray-600">טוען אירועים...</p>}
      {error && <p className="text-red-500 text-center">{error}</p>}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {events.map((event) => (
          <div key={event.id} className="bg-white rounded-xl shadow p-4 space-y-2">
            <h3 className="text-xl font-semibold text-blue-800">{event.title}</h3>
            <p className="text-sm text-gray-600">{event.location}</p>
            <p className="text-sm">מדווח: {event.reporter}</p>
            <p className="text-sm">משתתפים: {event.people_count || 0}</p>
            <div className="flex gap-2">
              <button
                onClick={() => updateCount(event.id, +1)}
                className="bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded-lg"
              >
                ➕
              </button>
              <button
                onClick={() => updateCount(event.id, -1)}
                className="bg-yellow-500 hover:bg-yellow-600 text-white px-3 py-1 rounded-lg"
              >
                ➖
              </button>
              <button
                onClick={() => handleDelete(event.id)}
                className="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded-lg ml-auto"
              >
                מחק
              </button>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-8">
        <MapContainer center={[31.0461, 34.8516]} zoom={7} style={{ height: "400px", width: "100%" }}>
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
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
