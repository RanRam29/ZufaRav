import { FaTrashAlt } from "react-icons/fa";
import { FaCheckSquare } from "react-icons/fa";

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
  if (!event || !event.lat || !event.lng || !event.title) {
    return null;
  }

  const distance = getDistance(userLocation, event);
  const textColor = getTextColorByDistance(distance);
  const backgroundClass = getBackgroundClass(event);
  const timeLabel = getTimeLabel(event.datetime);
  const peopleCount = event.people_count ?? 0;

  return (
    <div
      className={`p-4 rounded-xl shadow-md transition-all border border-gray-300 ${
        isNew ? "animate-pulse border-green-400" : ""
      } ${backgroundClass}`}
    >
      <h2 className="text-xl font-bold mb-2">{event.title}</h2>
      <p>כתובת: {event.address}</p>
      <p>מדווח: {event.reporter}</p>
      <p>
        סטטוס:
        {event.confirmed ? (
          <span className="text-green-600 font-bold"> מאושר ✅</span>
        ) : (
          <button
            onClick={() => confirmEvent(event.id)}
            className="text-blue-600 font-bold"
          >
            אשר <FaCheckSquare className="inline" />
          </button>
        )}
      </p>
      <p>בהמתנה: {timeLabel}</p>
      <p>📍 מרחק: <span className={textColor}>{distance} ק״מ</span></p>
      <p>משתתפים: {peopleCount}</p>

      <button
        className="bg-red-500 text-white px-4 py-1 mt-3 rounded hover:bg-red-600 transition"
        onClick={() => deleteEvent(event.id)}
      >
        מחק <FaTrashAlt className="inline" />
      </button>
    </div>
  );
}
