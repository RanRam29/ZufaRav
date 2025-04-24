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
  newEventIds = []  // קבל את המידע של האירועים החדשים
}) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
      {events.map(event => (
        <EventCard
          key={event.id || event.title}  // השתמש במזהה הייחודי אם קיים
          event={event}
          isNew={newEventIds.includes(event.id)}  // העבר את isNew ל־EventCard
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
