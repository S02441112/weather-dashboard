import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

import requests

DEFAULT_LAT = 38.835223497138934
DEFAULT_LON = -104.80464085663371

def query_openmeteo(latitude: float | None = None, longitude: float | None = None):
    lat = DEFAULT_LAT if latitude is None else latitude
    lon = DEFAULT_LON if longitude is None else longitude

    # Set up the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "weather_code"],
        "timezone": "America/Denver",
        "wind_speed_unit": "mph",
        "temperature_unit": "fahrenheit",
        "precipitation_unit": "inch",
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    # TODO return this instead of printing
    response = responses[0]
    print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation: {response.Elevation()} m asl")
    print(f"Timezone: {response.Timezone()}{response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
    daily_precipitation_sum = daily.Variables(2).ValuesAsNumpy()
    daily_weather_code = daily.Variables(3).ValuesAsNumpy()

    daily_data = {
        "date": pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=True),
            end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left"
        ).tz_convert(response.Timezone().decode())
    }

    daily_data["temperature_2m_max"] = daily_temperature_2m_max
    daily_data["temperature_2m_min"] = daily_temperature_2m_min
    daily_data["precipitation_sum"] = daily_precipitation_sum
    daily_data["weather_code"] = daily_weather_code

    daily_dataframe = pd.DataFrame(data=daily_data)

    return daily_dataframe.to_dict(orient="records")


def format_weather_data(api_weather_data):

    weather_code_json = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Light freezing drizzle",
        57: "Dense freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snowfall",
        73: "Moderate snowfall",
        75: "Heavy snowfall",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        97: "Heavy thunderstorm",
        99: "Thunderstorm with heavy hail"
    }

    formatted_weather_data = []

    for day in api_weather_data:
        formatted_data = {
            "day": day["date"],
            # round temp max and min to nearest whole
            "max_temp": round(day["temperature_2m_max"]),
            "min_temp": round(day["temperature_2m_min"]),
            # round precipitation sum to 2 decimal places
            "precipitation_sum": round(day["precipitation_sum"], 2),
            # assign weather codes dict keys to their values and use unknown as safety net
            "weather_code": weather_code_json.get(int(day["weather_code"]), "Unknown"),
        }

        formatted_weather_data.append(formatted_data)

    return formatted_weather_data

# Input: city name str, Output: dict with latitude, longitude, name, country
def geocode_location(city):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city, "count": 1, "language": "en", "format": "json"}
    request = requests.get(url, params=params)
    data = request.json() # Converts JSON data into Python dict

    if not data.get("results"):
        return None

    result = data["results"][0]
    return {
            "latitude": result["latitude"],
            "longitude": result["longitude"],
            "name": result["name"],
            "country": result["country"]
    }

def geocode_search():
    print("TODO: Implement geocode_search function to search for place names and return coordinates")

def validate_place(place_name):
    if place_name is None or not isinstance(place_name, str) or place_name.strip() == "":
        return False
    print("TODO: Implement validate_place function to check if place name is valid")
    return True