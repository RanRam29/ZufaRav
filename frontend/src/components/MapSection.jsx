import { MapContainer, TileLayer, Marker, Popup, Circle } from "react-leaflet";

export default function MapSection({ userLocation, events }) {
  return (
    <MapContainer center={[31.8, 35.2]} zoom={8} scrollWheelZoom={false} style={{ height: '400px', width: '100%' }}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      {userLocation && (
        <>
          <Marker position={[userLocation.lat, userLocation.lng]}>
            <Popup>המיקום שלך</Popup>
          </Marker>
          <Circle center={[userLocation.lat, userLocation.lng]} radius={100} pathOptions={{ color: 'blue' }} />
        </>
      )}
      {events.map((e, i) => (
        e.lat && e.lng && (
          <Marker key={i} position={[e.lat, e.lng]}>
            <Popup>
              <strong>{e.title}</strong><br />
              {e.address}<br />
              מדווח: {e.reporter}<br />
              סטטוס: {e.confirmed ? '✅' : '⏳'}
            </Popup>
          </Marker>
        )
      ))}
    </MapContainer>
  );
}