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
  newEventIds = []
}) {
  if (!Array.isArray(events)) {
    console.error("❌ EventsGrid קיבל events לא תקני:", events);
    return null;
  }

  const filtered = events.filter(
    (e) =>
      e &&
      typeof e.lat === "number" &&
      typeof e.lng === "number" &&
      !isNaN(e.lat) &&
      !isNaN(e.lng)
  );

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
      {filtered.map((event) => (
        <EventCard
          key={event.id || event.title}
          event={event}
          isNew={newEventIds.includes(event.id)}
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
