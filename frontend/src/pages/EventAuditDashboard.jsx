import { useEffect, useState } from "react";
import axios from "../axiosInstance";

export default function EventAuditDashboard() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchEvents();
  }, []);

  const fetchEvents = async () => {
    try {
      const res = await axios.get("/events/list");
      setEvents(res.data);
    } catch (err) {
      console.error("שגיאה בטעינת אירועים:", err);
    } finally {
      setLoading(false);
    }
  };

  const validateEvent = (event) => {
    if (!event.title || !event.reporter || !event.datetime) return false;
    return true;
  };

  return (
    <div className="p-6 bg-gray-100 min-h-screen text-right">
      <h1 className="text-2xl font-bold mb-4">דוח בדיקות אירועים</h1>
      {loading ? (
        <p>טוען...</p>
      ) : (
        <div className="space-y-4">
          {events.map((event, index) => {
            const isValid = validateEvent(event);
            return (
              <div
                key={index}
                className={`p-4 rounded-xl shadow ${isValid ? "bg-white" : "bg-red-100 border-red-400 border"}`}
              >
                <h2 className="text-xl font-bold">{event.title || "❌ כותרת חסרה"}</h2>
                <p>מדווח: {event.reporter || "❌ לא ידוע"}</p>
                <p>אישור: {event.confirmed ? "✅ מאושר" : "⏳ ממתין"}</p>
                <p>משתתפים: {event.people_count ?? 0}</p>
                <p>זמן יצירה: {new Date(event.datetime).toLocaleString("he-IL")}</p>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
