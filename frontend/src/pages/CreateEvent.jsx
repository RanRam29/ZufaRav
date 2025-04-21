import { useState } from "react";
import axios from "../axiosInstance";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

export default function CreateEvent({ onCreate }) {
  const [event, setEvent] = useState({
    title: "",
    location: "",
    severity: "LOW",
    people_count: 1,
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setEvent((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const reporter = localStorage.getItem("username");
    const timestamp = new Date().toISOString();

    if (!event.title || !event.location || !reporter) {
      toast.error("יש למלא את כל השדות הנדרשים");
      return;
    }

    try {
      await axios.post("/events/create", {
        ...event,
        reporter,
        datetime: timestamp,
      });

      toast.success("✅ האירוע נוצר בהצלחה!");
      if (onCreate) onCreate();

      setEvent({
        title: "",
        location: "",
        severity: "LOW",
        people_count: 1,
      });
    } catch (err) {
      console.error("שגיאה ביצירת אירוע:", err);
      toast.error("❌ שגיאה בעת יצירת האירוע");
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
          name="people_count"
          min="1"
          max="99"
          placeholder="כמות רבנים נדרשת"
          className="input"
          value={event.people_count}
          onChange={handleChange}
          required
        />

        <button type="submit" className="btn w-full bg-green-600 hover:bg-green-700 text-white">
          צור אירוע
        </button>
      </form>
    </div>
  );
}