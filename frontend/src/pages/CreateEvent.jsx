import { useState } from "react";
import axios from "../axiosInstance";
import { toast, ToastContainer } from "react-toastify";
import { useNavigate } from "react-router-dom";
import {
  geocodeAddress,
  getLocalISOTime,
  validateForm,
} from "../utils/utility";
import "react-toastify/dist/ReactToastify.css";

export default function CreateEvent({ onCreate }) {
  const [event, setEvent] = useState({
    title: "",
    location: "",
    severity: "LOW",
    people_required: 1, // ✅ תואם לשם ב-backend
  });

  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setEvent((prev) => ({ ...prev, [name]: value }));
    console.debug(`✏️ שדה שונה: ${name} = ${value}`);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const reporter = localStorage.getItem("username");
    if (!reporter) {
      console.error("❌ אין משתמש מחובר (localStorage)");
      toast.error("אין משתמש מחובר. התחבר שוב.");
      navigate("/login");
      return;
    }

    if (!validateForm(event)) {
      toast.error("יש למלא את כל השדות הנדרשים");
      return;
    }

    try {
      console.debug("📍 מתחיל תהליך המרת כתובת לקואורדינטות...");
      const coords = await geocodeAddress(event.location);

      if (!coords) {
        toast.error("⚠️ כתובת לא מזוהה. נסה לנסח אותה אחרת");
        console.warn("⚠️ קואורדינטות לא אותרו. עצירת התהליך");
        return;
      }

      const localISOTime = getLocalISOTime();

      const eventPayload = {
        ...event,
        reporter,
        address: event.location,
        datetime: localISOTime,
        lat: coords.lat,
        lng: coords.lng,
        people_count: 0, // ✅ חובה לפי המודל ב־backend
      };

      console.debug("🚀 שליחת אירוע חדש לשרת:", eventPayload);

      await axios.post("/events/create", eventPayload);

      toast.success("✅ האירוע נוצר בהצלחה!");
      setTimeout(() => {
        navigate("/dashboard");
      }, 1200);
    } catch (err) {
      console.error("❌ שגיאה ביצירת האירוע:", err);
      toast.error("❌ שגיאה בעת יצירת האירוע. ודא שהכתובת תקינה.");
    }
  };

  return (
    <div className="space-y-4 bg-white p-4 rounded-xl shadow-md">
      <ToastContainer position="top-center" />
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          name="title"
          placeholder="כותרת"
          className="input"
          value={event.title}
          onChange={handleChange}
          required
        />
        <input
          name="location"
          placeholder="כתובת האירוע"
          className="input"
          value={event.location}
          onChange={handleChange}
          required
        />
        <select
          name="severity"
          className="input"
          value={event.severity}
          onChange={handleChange}
          required
        >
          <option value="LOW">נמוכה</option>
          <option value="MEDIUM">בינונית</option>
          <option value="HIGH">גבוהה</option>
        </select>
        <input
          type="number"
          name="people_required"
          min="1"
          max="99"
          placeholder="כמות רבנים נדרשת"
          className="input"
          value={event.people_required}
          onChange={handleChange}
          required
        />
        <button
          type="submit"
          className="btn w-full bg-green-600 hover:bg-green-700 text-white"
        >
          צור אירוע
        </button>
      </form>
    </div>
  );
}
