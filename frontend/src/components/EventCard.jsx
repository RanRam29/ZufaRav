export default function EventCard({
  event = {},
  userLocation,
  getDistance,
  getTextColorByDistance,
  getBackgroundClass,
  getTimeLabel,
  confirmEvent,
  deleteEvent,
  isNew
}) {
  const {
    id,
    title = "ללא כותרת",
    address,
    location,
    reporter = "לא ידוע",
    confirmed = false,
    people_count = 0,
    datetime,
    lat,
    lng
  } = event;

  const dist =
    userLocation && lat != null && lng != null
      ? getDistance(userLocation.lat, userLocation.lng, lat, lng)
      : null;

  const distText = dist != null
    ? dist < 1000
      ? `${Math.round(dist)} מטר`
      : `${(dist / 1000).toFixed(2)} ק״מ`
    : null;

  console.debug("🧩 Rendering EventCard", { event });

  return (
    <div
      key={id || title}
      className={`relative rounded-xl p-4 shadow transition-all duration-500 ${getBackgroundClass(event)} ${
        isNew ? "border-4 border-blue-500 animate-pulse" : ""
      }`}
    >
      {isNew && (
        <div className="absolute top-0 right-0 bg-blue-500 text-white text-xs px-2 py-1 rounded-bl-lg animate-bounce">
          חדש!
        </div>
      )}

      <h3 className="text-lg font-bold">{title}</h3>
      <p>כתובת: {address || location || "—"}</p>
      <p>מדווח: {reporter}</p>
      <p>סטטוס: {confirmed ? "✅ מאושר" : "⏳ ממתין"}</p>
      <p>בהמתנה: {datetime ? getTimeLabel(datetime) : "—"}</p>
      <p>משתתפים: {people_count}</p>
      {distText && <p className={`${getTextColorByDistance(dist)}`}>📍 מרחק: {distText}</p>}

      <div className="flex gap-2 mt-2">
        {!confirmed && (
          <button
            onClick={() => confirmEvent(title)}
            className="bg-purple-600 text-white px-2 rounded"
          >
            מאשר הגעה
          </button>
        )}
        <button
          onClick={() => deleteEvent(id)}
          className="bg-red-500 text-white px-2 rounded"
        >
          מחק
        </button>
      </div>
    </div>
  );
}
