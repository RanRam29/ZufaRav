import React from "react";
import EventCard from "./EventCard";

const EventsGrid = ({ events, onConfirm, onDelete, filterStatus, loading }) => {
  if (loading) {
    return <div className="text-center text-gray-500 mt-4">⏳ טוען אירועים...</div>;
  }

  if (!events || events.length === 0) {
    return <div className="text-center text-gray-500 mt-4">אין אירועים להצגה.</div>;
  }

  const validEvents = events
    .filter((event) => {
      const lat = parseFloat(event.lat);
      const lng = parseFloat(event.lng);
      const hasValidLatLng = !isNaN(lat) && !isNaN(lng);
      const hasTitle = typeof event.title === "string" && event.title.trim() !== "";
      const isFake =
        event.title?.toLowerCase() === "title" &&
        (event.lat === "lat" || event.lng === "lng");

      const isIncomplete = !event.id || !event.created_at;

      if (!hasValidLatLng || !hasTitle || isFake || isIncomplete) {
        console.warn("⚠️ אירוע סונן בגלל ערכים שגויים:", event);
        return false;
      }

      return true;
    })
    .sort((a, b) => new Date(b.created_at) - new Date(a.created_at));

  const filteredEvents = validEvents.filter((event) => {
    if (filterStatus === "pending") return !event.confirmed;
    if (filterStatus === "confirmed") return event.confirmed;
    return true;
  });

  if (filteredEvents.length === 0) {
    return <div className="text-center text-gray-400 mt-4">לא נמצאו אירועים לפי הסינון.</div>;
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 mt-4 px-2">
      {filteredEvents.map((event) => (
        <EventCard
          key={event.id}
          event={event}
          onConfirm={onConfirm}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
};

export default EventsGrid;
