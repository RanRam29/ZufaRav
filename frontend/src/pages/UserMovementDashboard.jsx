import { useEffect, useRef } from "react";
import { MapContainer, TileLayer, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import "leaflet.heat";
import { useNavigate } from "react-router-dom";

function HeatLayer({ points }) {
  const map = useMap();
  const heatLayerRef = useRef(null);

  useEffect(() => {
    if (!map) return;

    if (heatLayerRef.current) {
      map.removeLayer(heatLayerRef.current);
    }

    const heatLayer = window.L.heatLayer(points, {
      radius: 25,
      blur: 15,
      maxZoom: 17,
    }).addTo(map);

    heatLayerRef.current = heatLayer;
  }, [points, map]);

  return null;
}

export default function UserMovementDashboard() {
  const navigate = useNavigate();
  const generateFakeData = () =>
    Array.from({ length: 30 }, () => [
      31.0461 + Math.random() * 2 - 1,
      34.8516 + Math.random() * 2 - 1,
      Math.random() * 0.8 + 0.2,
    ]);

  const points = generateFakeData();

  return (
    <div className="min-h-screen bg-gray-100 p-6 text-right">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-800">דשבורד תנועה - Heatmap</h1>
        <button
          onClick={() => navigate("/dashboard")}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-xl"
        >
          חזרה לדשבורד האירועים
        </button>
      </div>

      <MapContainer center={[31.0461, 34.8516]} zoom={8} style={{ height: "600px", width: "100%" }}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        <HeatLayer points={points} />
      </MapContainer>
    </div>
  );
}
