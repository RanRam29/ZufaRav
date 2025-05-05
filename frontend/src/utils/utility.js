export async function geocodeAddress(address) {
  try {
    const response = await fetch(
      `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}`,
      {
        headers: {
          "User-Agent": "ZufaRavApp/1.0 (+https://zufa-rav.vercel.app)",
        },
      }
    );
    const data = await response.json();

    if (!Array.isArray(data) || data.length === 0) {
      console.warn("⚠️ No coordinates found for address:", address);
      return null;
    }

    return {
      lat: parseFloat(data[0].lat),
      lng: parseFloat(data[0].lon),
    };
  } catch (error) {
    console.error("❌ Error during geocoding:", error);
    return null;
  }
}

export function getLocalISOTime() {
  const now = new Date();
  const timezoneOffsetMs = now.getTimezoneOffset() * 60000;
  return new Date(now.getTime() - timezoneOffsetMs).toISOString().slice(0, -1);
}

export function validateForm(event) {
  if (!event.title || !event.location) {
    console.warn("⚠️ Missing required fields: title or location");
    return false;
  }
  return true;
}
