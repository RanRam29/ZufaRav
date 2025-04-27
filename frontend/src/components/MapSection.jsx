import { MapContainer, TileLayer, Marker, Popup, Circle } from "react-leaflet";
import L from "leaflet";

// אייקונים כמו שכבר התקנו (ירוק/צהוב/אדום)

export default function MapSection({ userLocation, events, newEventIds = [] }) {
  console.debug("🗺️ Rendering MapSection...", { userLocation, numberOfEvents: events?.length || 0 });

  if (!events) {
    console.error("❌ No events data provided to MapSection!");
    return <p className="text-center text-red-600">שגיאה בטעינת המפה</p>;
  }

  return (
    <MapContainer
      center={[31.8, 35.2]}
      zoom={8}
      scrollWheelZoom={true}
      style={{ height: '400px', width: '100%' }}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="&copy; OpenStreetMap contributors"
      />

      {userLocation && (
        <>
          <Marker
            position={[userLocation.lat, userLocation.lng]}
            icon={userIcon}
          >
            <Popup>המיקום שלך</Popup>
          </Marker>
          <Circle center={[userLocation.lat, userLocation.lng]} radius={100} pathOptions={{ color: 'blue' }} />
          {console.debug("📍 User location rendered:", userLocation)}
        </>
      )}

      {events.map((e, i) => {
        let iconToUse = pendingIcon;

        if (e.arrival_time) {
          iconToUse = arrivedIcon;
        } else if (e.confirmed) {
          iconToUse = confirmedIcon;
        }

        return (e.lat && e.lng ? (
          <Marker key={i} position={[e.lat, e.lng]} icon={iconToUse}>
            <Popup>
              <strong>{e.title}</strong><br />
              {e.address || e.location}<br />
              מדווח: {e.reporter}<br />
              סטטוס: {e.confirmed ? (e.arrival_time ? '✅ הגיע' : '✅ מאושר') : '⏳ ממתין'}
            </Popup>
          </Marker>
        ) : (
          console.warn(`⚠️ Event without valid coordinates:`, e)
        ));
      })}
    </MapContainer>
  );
}
