# API Routes
# health page to determine if services are up
from fastapi import APIRouter
from app.services.weather import query_openmeteo

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