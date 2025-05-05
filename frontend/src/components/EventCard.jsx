import { FaTrashAlt, FaCheckSquare } from "react-icons/fa";

export default function EventCard({
  event,
  isNew = false,
  userLocation,
  getDistance,
  getTextColorByDistance,
  getBackgroundClass,
  getTimeLabel,
  confirmEvent,
  deleteEvent
}) {
  if (
    !event ||
    typeof event.lat !== "number" ||
    typeof event.lng !== "number" ||
    !event.title
  ) {
    console.warn("⛔ אירוע לא תקין - לא יוצג:", event);
    return null;
  }

  const distance = getDistance(userLocation, event);
  const peopleCount = typeof event.people_count === "number" ? event.people_count : 0;
  const backgroundClass = getBackgroundClass(event);
  const textColor = getTextColorByDistance(distance);
  const timeLabel = getTimeLabel(event.datetime);

  return (
    <div
      className={`p-4 rounded-xl shadow-md transition-all border border-gray-300 ${
        isNew ? "animate-pulse border-green-400" : ""
      } ${backgroundClass}`}
    >
      <h2 className="text-xl font-bold mb-2">{event.title}</h2>
      <p>כתובת: {event.address || "ללא כתובת"}</p>
      <p>מדווח: {event.reporter || "לא ידוע"}</p>

      <p>
        סטטוס:
        {event.confirmed ? (
          <span className="text-green-600 font-bold"> מאושר ✅</span>
        ) : (
          <button
            onClick={() => confirmEvent(event.id)}
            className="text-blue-600 font-bold ml-1"
          >
            אשר <FaCheckSquare className="inline" />
          </button>
        )}
      </p>

      <p>⏱ זמן: {timeLabel}</p>
      <p>
        📍 מרחק: <span className={textColor}>{distance} ק״מ</span>
      </p>
      <p>👥 משתתפים: {peopleCount}</p>

      <button
        className="bg-red-500 text-white px-4 py-1 mt-3 rounded hover:bg-red-600 transition"
        onClick={() => deleteEvent(event.id)}
      >
        מחק <FaTrashAlt className="inline" />
      </button>
    </div>
  );
}
