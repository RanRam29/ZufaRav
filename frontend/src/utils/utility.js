export async function geocodeAddress(address) {
    try {
      const response = await fetch(
        `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}`
      );
      const data = await response.json();
      if (data.length > 0) {
        return {
          lat: parseFloat(data[0].lat),
          lng: parseFloat(data[0].lon),
        };
      }
      console.warn("⚠️ No coordinates found for address:", address);
      return { lat: 0, lng: 0 };
    } catch (error) {
      console.error("❌ Error during geocoding:", error);
      return { lat: 0, lng: 0 };
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