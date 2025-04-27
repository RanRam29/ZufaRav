export default function EventCard({
  event,
  userLocation,
  getDistance,
  getTextColorByDistance,
  getBackgroundClass,
  getTimeLabel,
  confirmEvent,
  deleteEvent,
  isNew
}) {
  const dist = userLocation && event.lat && event.lng
    ? getDistance(userLocation.lat, userLocation.lng, event.lat, event.lng)
    : null;
  const distText = dist < 1000 ? `${Math.round(dist)} מטר` : `${(dist / 1000).toFixed(2)} ק״מ`;

  console.debug("🧩 Rendering EventCard", { event });

  return (
    <div
      key={event.id || event.title}
      className={`relative rounded-xl p-4 shadow transition-all duration-500 ${getBackgroundClass(event)} ${isNew ? "border-4 border-blue-500 animate-pulse" : ""}`}
    >
      {isNew && (
        <div className="absolute top-0 right-0 bg-blue-500 text-white text-xs px-2 py-1 rounded-bl-lg animate-bounce">
          חדש!
        </div>
      )}
      <h3 className="text-lg font-bold">{event.title}</h3>
      <p>כתובת: {event.address || event.location || "—"}</p> {/* ✅ תוספת כתובת */}
      <p>מדווח: {event.reporter}</p>
      <p>סטטוס: {event.confirmed ? "✅ מאושר" : "⏳ ממתין"}</p>
      <p>בהמתנה: {getTimeLabel(event.datetime)}</p>
      <p>משתתפים: {event.people_count || 0}</p>
      {dist && <p className={`${getTextColorByDistance(dist)}`}>📍 מרחק: {distText}</p>}
      <div className="flex gap-2 mt-2">
        {!event.confirmed && (
          <button onClick={() => confirmEvent(event.title)} className="bg-purple-600 text-white px-2 rounded">מאשר הגעה</button>
        )}
        <button onClick={() => deleteEvent(event.id)} className="bg-red-500 text-white px-2 rounded">מחק</button>
      </div>
    </div>
  );
}
