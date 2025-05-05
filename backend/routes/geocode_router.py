from fastapi import APIRouter, HTTPException, Query
import httpx

router = APIRouter()

@router.get("/geocode")
async def geocode_address(address: str = Query(..., min_length=3)):
    try:
        async with httpx.AsyncClient() as client:
            url = f"https://nominatim.openstreetmap.org/search?format=json&q={address}"
            headers = {"User-Agent": "ZufaRav/1.0 (admin@zufarav.example)"}
            response = await client.get(url, headers=headers)
            data = await response.json()

        if not data:
            raise HTTPException(status_code=404, detail="כתובת לא נמצאה")

        first_result = data[0]
        return {
            "lat": float(first_result["lat"]),
            "lng": float(first_result["lon"]),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"שגיאה בשירות גיאוקודינג: {str(e)}")
