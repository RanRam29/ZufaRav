import React from "react";

const EventCard = ({ event, onDelete, onConfirm }) => {
  const {
    id,
    title = "ללא כותרת",
    location = "",
    reporter = "",
    severity = "",
    confirmed = false,
    confirmed_at,
    confirmed_by,
    created_at,
    address = "",
    people_count = 0,
    lat,
    lng,
  } = event;

  // המרה והגנה על ערכים
  const parsedLat = parseFloat(lat);
  const parsedLng = parseFloat(lng);
  const isValidLatLng = !isNaN(parsedLat) && !isNaN(parsedLng);

  if (!isValidLatLng) {
    console.warn("⚠️ לא נמצא ערך תקין של lat/lng", event);
    return null;
  }

  return (
    <div className="bg-white rounded-2xl shadow p-4 mb-4 border border-gray-300">
      <h2 className="text-lg font-bold mb-1">{title}</h2>
      <p>כתובת: {address}</p>
      <p>מדווח: {reporter}</p>
      <p>
        סטטוס:{" "}
        {confirmed ? (
          <span className="text-green-600 font-bold">מאושר ✅</span>
        ) : (
          <span className="text-yellow-600 font-bold">ממתין לאישור ⏳</span>
        )}
      </p>
      {confirmed_at && (
        <p>
          אושר ע"י {confirmed_by} בתאריך:{" "}
          {new Date(confirmed_at).toLocaleString("he-IL")}
        </p>
      )}
      <p>
        נוצר בתאריך: {new Date(created_at).toLocaleString("he-IL")}
      </p>
      <p>רמת חומרה: {severity}</p>
      <p>משתתפים: {isNaN(people_count) ? 0 : people_count}</p>
      <div className="flex justify-end mt-2">
        {!confirmed && (
          <button
            onClick={() => onConfirm(id)}
            className="bg-green-500 hover:bg-green-600 text-white px-4 py-1 rounded ml-2"
          >
            אשר
          </button>
        )}
        <button
          onClick={() => onDelete(id)}
          className="bg-red-500 hover:bg-red-600 text-white px-4 py-1 rounded"
        >
          מחק
        </button>
      </div>
    </div>
  );
};

export default EventCard;
