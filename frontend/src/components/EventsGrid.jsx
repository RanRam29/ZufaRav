import React from "react";
import EventCard from "./EventCard";

export default function EventsGrid({
  events,
  userLocation,
  getDistance,
  getTextColorByDistance,
  getBackgroundClass,
  getTimeLabel,
  onDelete,
  onConfirm,
}) {
  if (!Array.isArray(events)) {
    console.error("🚫 events is not an array:", events);
    return null;
  }

  const validEvents = events
    .filter((event) => {
      const lat = parseFloat(event.lat);
      const lng = parseFloat(event.lng);
      const hasValidLatLng = !isNaN(lat) && !isNaN(lng);
      const hasTitle = typeof event.title === "string" && event.title.trim() !== "";

      if (!hasValidLatLng || !hasTitle) {
        console.warn("⚠️ אירוע עם בעיה בסינון lat/lng/title:", event);
        return false;
      }

      return true;
    })
    .sort((a, b) => new Date(b.created_at) - new Date(a.created_at));

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4">
      {validEvents.length === 0 ? (
        <p className="text-gray-500 text-center col-span-full">אין אירועים להצגה</p>
      ) : (
        validEvents.map((event) => (
          <EventCard
            key={event.id}
            event={event}
            userLocation={userLocation}
            getDistance={getDistance}
            getTextColorByDistance={getTextColorByDistance}
            getBackgroundClass={getBackgroundClass}
            getTimeLabel={getTimeLabel}
            confirmEvent={onConfirm}
            deleteEvent={onDelete}
          />
        ))
      )}
    </div>
  );
}
