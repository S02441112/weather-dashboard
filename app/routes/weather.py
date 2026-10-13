# API Routes
# health page to determine if services are up
from fastapi import APIRouter
from app.services.weather import query_openmeteo, geocode_search

router = APIRouter()

@router.get("/health")
def read_health():
    health_message = {"status": "ok"}
    return health_message


# display raw json from openmeteo
@router.get("/api/weather")
def read_weather_api():
    weather_data = query_openmeteo()
    return weather_data


router.get("/api/cities")
async def api_cities(q: str):
    if not q or len(q) < 2:
        return []
    results = geocode_search(q)
    return results
