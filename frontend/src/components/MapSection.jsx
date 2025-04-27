import { MapContainer, TileLayer, Marker, Popup, Circle } from "react-leaflet";
import L from "leaflet";

// אייקון סיכה ירוקה למשתמש
const userIcon = new L.Icon({
  iconUrl: "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowUrl: "https://unpkg.com/leaflet@1.9.3/dist/images/marker-shadow.png",
  shadowSize: [41, 41],
});

// אייקון דגל אדום לאירועים
const eventIcon = new L.Icon({
  iconUrl: "https://cdn-icons-png.flaticon.com/512/684/684908.png", // אייקון דגל אדום קטן
  iconSize: [30, 30],
  iconAnchor: [15, 30],
  popupAnchor: [0, -30],
});

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

      {events.map((e, i) => (
        e.lat && e.lng ? (
          <Marker key={i} position={[e.lat, e.lng]} icon={eventIcon}>
            <Popup>
              <strong>{e.title}</strong><br />
              {e.address}<br />
              מדווח: {e.reporter}<br />
              סטטוס: {e.confirmed ? '✅' : '⏳'}
            </Popup>
          </Marker>
        ) : (
          console.warn(`⚠️ Event without valid coordinates:`, e)
        )
      ))}
    </MapContainer>
  );
}
