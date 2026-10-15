from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services.weather import query_openmeteo, format_weather_data, geocode_location


BASE_DIR = Path(__file__).resolve().parent.parent
router = APIRouter()

templates = Jinja2Templates(directory=BASE_DIR / "templates")

# request root directory and display formatted weather information from weather api
@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    api_weather_data = query_openmeteo()
    weather_data = format_weather_data(api_weather_data)
    return templates.TemplateResponse(request, "index.html", {"weather_data": weather_data})

@router.post("/", response_class=HTMLResponse)
async def search_place(request: Request):
    form_data = await request.form()
    city = (form_data.get("city-input") or "").strip()

    # If the city input is empty, return the index page with a message prompting the user to enter a city name
    if not city:
        # api_weather_data = query_openmeteo() #  returns default {"latitude": ..., "longitude": ...}
        return templates.TemplateResponse(request, "index.html", {"weather_data": [], "city_input": "", "warning_message": "Please enter a city name."})

    # If the city input is not empty, geocode the location to get its coordinates
    coords = geocode_location(city)
    # If the geocoding fails (i.e., no coordinates are found), return the index page with a message indicating that no results were found for the entered city
    if not coords:
        return templates.TemplateResponse(request, "index.html", {"weather_data": [], "city_input": city, "warning_message": f"No results for '{city}'. Please try another city."})

    # If the geocoding is successful, query the weather data for the obtained coordinates and format it for display
    api_weather_data = query_openmeteo(latitude=coords["latitude"], longitude=coords["longitude"])
    weather_data = format_weather_data(api_weather_data)

    return templates.TemplateResponse(request, "index.html", {"weather_data": weather_data, "city_input": city, "message": f"Showing weather for {city}."})
