from fastapi import APIRouter, HTTPException, Query
import httpx
from app.config.logger import logger  # ודא שיש לך את זה

router = APIRouter()

@router.get("/geocode")
async def geocode_address(address: str = Query(..., min_length=3)):
    logger.debug(f"📡 קיבלה בקשת גיאוקודינג לכתובת: {address}")
    try:
        async with httpx.AsyncClient() as client:
            url = f"https://nominatim.openstreetmap.org/search?format=json&q={address}"
            headers = {"User-Agent": "ZufaRav/1.0 (admin@zufarav.example)"}
            response = await client.get(url, headers=headers)
            data = await response.json()

        if not data:
            logger.warning(f"⚠️ כתובת לא נמצאה: {address}")
            raise HTTPException(status_code=404, detail="⚠️ הכתובת לא נמצאה")

        first_result = data[0]
        logger.info(f"✅ נמצא מיקום: {first_result['lat']}, {first_result['lon']}")
        return {
            "lat": float(first_result["lat"]),
            "lng": float(first_result["lon"]),
        }

    except httpx.HTTPError as e:
        logger.error(f"❌ שגיאת HTTP במהלך בקשת גיאוקודינג: {str(e)}")
        raise HTTPException(status_code=502, detail="שגיאת תקשורת עם שרת הגיאוקודינג")
    except Exception as e:
        logger.error(f"❌ שגיאה כללית בגיאוקודינג: {str(e)}")
        raise HTTPException(status_code=500, detail=f"שגיאה בשירות גיאוקודינג: {str(e)}")
