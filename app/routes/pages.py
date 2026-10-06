from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services.weather import query_openmeteo, format_weather_data


BASE_DIR = Path(__file__).resolve().parent.parent
router = APIRouter()

templates = Jinja2Templates(directory=BASE_DIR / "templates")

# request root directory and display formatted weather information from weather api
@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    api_weather_data = query_openmeteo()
    weather_data = format_weather_data(api_weather_data)
    return templates.TemplateResponse(request, "index.html", {"weather_data": weather_data})
