import EventCard from "./EventCard";

export default function EventsGrid({
  events,
  userLocation,
  getDistance,
  getTextColorByDistance,
  getBackgroundClass,
  getTimeLabel,
  confirmEvent,
  deleteEvent,
}) {
  if (!Array.isArray(events)) return <p>אין אירועים להצגה.</p>;

  const validEvents = events.filter((event) => {
    const isValid =
      event &&
      typeof event.lat === "number" &&
      typeof event.lng === "number" &&
      typeof event.title === "string";

    if (!isValid) {
      console.warn("⚠️ אירוע עם lat/lng לא תקינים סונן:", event);
    }

    return isValid;
  });

  if (validEvents.length === 0) return <p>לא נמצאו אירועים תקינים.</p>;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4">
      {validEvents.map((event) => (
        <EventCard
          key={event.id}
          event={event}
          userLocation={userLocation}
          getDistance={getDistance}
          getTextColorByDistance={getTextColorByDistance}
          getBackgroundClass={getBackgroundClass}
          getTimeLabel={getTimeLabel}
          confirmEvent={confirmEvent}
          deleteEvent={deleteEvent}
        />
      ))}
    </div>
  );
}
