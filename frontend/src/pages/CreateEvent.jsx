import { useState } from "react";
import axios from "../axiosInstance";

export default function CreateEvent({ onCreate }) {
  const [event, setEvent] = useState({
    title: "",
    location: "",
    severity: "LOW",
    people_count: 1,
    date: "",
    time: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setEvent((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const reporter = localStorage.getItem("username");
    const timestamp = new Date(`${event.date}T${event.time}`).toISOString();

    try {
      await axios.post("/events/create", {
        ...event,
        reporter,
        datetime: timestamp,
      });

      onCreate(); // עדכון רשימת האירועים
    } catch (err) {
      alert("שגיאה ביצירת אירוע");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 bg-white p-4 rounded-xl shadow-md">
      <input name="title" placeholder="כותרת" className="input" onChange={handleChange} required />
      <input name="location" placeholder="כתובת האירוע" className="input" onChange={handleChange} required />
      <select name="severity" className="input" onChange={handleChange} required>
        <option value="LOW">נמוכה</option>
        <option value="MEDIUM">בינונית</option>
        <option value="HIGH">גבוהה</option>
      </select>
      <input type="number" name="people_count" min="1" max="99" placeholder="כמות רבנים נדרשת" className="input" onChange={handleChange} required />
      <input type="date" name="date" className="input" onChange={handleChange} required />
      <input type="time" name="time" className="input" onChange={handleChange} required />
      <button type="submit" className="btn">צור אירוע</button>
    </form>
  );
}
