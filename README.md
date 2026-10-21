# Weather Dashboard

A Python-based weather dashboard built with **FastAPI**, **Jinja2**, and the **Open-Meteo API**. The application retrieves a seven-day forecast and displays daily weather information in a browser. Users can search for a city to view its forecast, while API endpoints provide access to raw and formatted weather data.

This repository is developed incrementally through project sprints to practice Python development, API integration, server-side rendering, application structure, and deployment.

## Project Status

- **Current milestone:** Sprint 2
- **Application:** FastAPI web application
- **Weather provider:** Open-Meteo
- **Forecast:** Seven-day daily forecast

## Features

- **Seven-day forecast:** Displays daily weather information for the selected location.
- **City search:** Search for a city by name using the dashboard form.
- **Location geocoding:** Uses the Open-Meteo Geocoding API to resolve a city name to geographic coordinates.
- **Daily weather details:**
  - Maximum temperature in Fahrenheit
  - Minimum temperature in Fahrenheit
  - Total precipitation in inches
  - Human-readable weather conditions
- **Weather-code formatting:** Converts Open-Meteo weather codes into readable descriptions such as *Clear sky*, *Overcast*, and *Moderate rain*.
- **API endpoints:** Provides raw weather data, formatted weather data, city lookup, and a health-check endpoint.
- **Resilient API requests:** Uses response caching and retry handling for forecast requests.
- **Server-rendered interface:** Uses Jinja2 templates to render weather data into HTML.
- **Static styling:** Serves CSS files through FastAPI.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and data processing |
| FastAPI | Web framework and API routes |
| Uvicorn | ASGI server used to run the application |
| Open-Meteo Forecast API | Daily forecast data |
| Open-Meteo Geocoding API | Resolves city names to coordinates |
| Pandas | Processes forecast dates and weather values |
| Jinja2 | Renders server-side HTML templates |
| Requests | Sends HTTP requests to the geocoding API |
| Requests Cache | Caches forecast API responses |
| Retry Requests | Retries forecast requests after failures |
| HTML and CSS | Browser interface and styling |
| `uv` | Python dependency and project management |

## How It Works

The application separates page handling, weather API routes, and weather data processing.

```text
Browser
   |
   | Visit dashboard or submit city search
   v
FastAPI application
   |
   +----------------------------+
   |                            |
   v                            v
Page routes                 Weather API routes
   |                            |
   v                            +--> /api/weather
Weather service                 +--> /api/weather/formatted
   |                            +--> /api/cities/{q}
   |
   +--> Geocoding API (for city searches)
   |
   +--> Open-Meteo Forecast API
   |
   v
Process and format daily forecast
   |
   v
Jinja2 HTML template
   |
   v
Weather displayed in browser
```

### Request and data flow

1. A visitor opens the dashboard or submits a city name.
2. For a city search, the application sends the name to the geocoding service and retrieves its coordinates.
3. The weather service requests the forecast for those coordinates.
4. Forecast values are processed and weather codes are converted to readable descriptions.
5. The page route passes the formatted data to a Jinja2 template.
6. The browser displays the forecast.

If a city search is empty or no matching location is found, the page displays a warning instead of attempting to show a forecast for the invalid search.

## Getting Started

### Prerequisites

- Python **3.14 or newer**, as specified in `pyproject.toml`
- [`uv`](https://docs.astral.sh/uv/) for project and dependency management
- An internet connection to retrieve forecast and geocoding data

### 1. Clone the repository

```bash
git clone https://github.com/S02441112/weather-dashboard.git
cd weather-dashboard
git switch Sprint2
```

If you already have the repository cloned, switch to the `Sprint2` branch from the project directory.

### 2. Install dependencies

The application imports several weather-service packages in addition to FastAPI and Jinja2. Ensure they are included in the project environment:

```bash
uv add "fastapi[standard]" jinja2 openmeteo-requests pandas requests-cache retry-requests requests
uv sync
```

If these dependencies have already been added to `pyproject.toml`, `uv sync` should be sufficient.

### 3. Start the application

From the repository root, run:

```bash
uv run uvicorn app.main:app --reload
```

Open the following address in a browser:

- Dashboard: <http://127.0.0.1:8000>
- Interactive API documentation: <http://127.0.0.1:8000/docs>
- Alternative API documentation: <http://127.0.0.1:8000/redoc>

To stop the development server, press `Ctrl+C` in the terminal.

### Run on a local network

To allow other devices on the same network to reach the application, run:

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Then visit `http://<server-local-ip>:8000` from another device, replacing `<server-local-ip>` with the host machine's local IP address.

**Security note:** Binding to `0.0.0.0` exposes the application on the host's network interfaces. Use this only on a network you trust, and configure firewall rules appropriately. This command alone does not make the application safely accessible from the public internet.

## API Reference

The application exposes the following routes.

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Renders the dashboard with the default location's forecast |
| `POST` | `/` | Processes a city search submitted through the dashboard form |
| `GET` | `/health` | Returns a simple health status |
| `GET` | `/api/weather` | Returns raw daily forecast records |
| `GET` | `/api/weather/formatted` | Returns forecast records formatted for display |
| `GET` | `/api/cities/{q}` | Searches for a city by name and returns geocoding results |

### Example responses

#### Health check

Request:

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

This is a basic application health endpoint. It does not independently verify that the external weather services are available.

#### Raw weather data

Request:

```http
GET /api/weather
```

Returns daily forecast records containing the date, maximum temperature, minimum temperature, precipitation total, and Open-Meteo weather code. The exact values depend on the location and forecast returned by the API.

#### Formatted weather data

Request:

```http
GET /api/weather/formatted
```

Returns forecast records with rounded temperature and precipitation values and human-readable weather descriptions. The route is intended to make the data easier for a client to consume.

#### City lookup

Request:

```http
GET /api/cities/Denver
```

Returns geocoding results for the supplied search term. Queries shorter than two characters return an empty list.

## Project Structure

```text
weather-dashboard/
├── app/
│   ├── main.py                 # Creates the FastAPI app and registers routes
│   ├── routes/
│   │   ├── pages.py            # Dashboard rendering and city-search form
│   │   └── weather.py          # Weather, formatted-data, and health endpoints
│   ├── services/
│   │   └── weather.py          # API calls, data processing, and geocoding
│   ├── templates/
│   │   └── index.html          # Jinja2 dashboard template
│   ├── static/
│   │   └── styles.css          # Dashboard styling
│   └── .cache/                 # Local API response cache (created at runtime)
├── pyproject.toml              # Project metadata and dependencies
├── uv.lock                     # Locked dependency versions
└── README.md
```

The cache directory may be created when the application runs and should not generally be committed to version control.

## Configuration and Data Handling

- The initial/default forecast uses coordinates defined in the weather service.
- City searches use the Open-Meteo Geocoding API to obtain coordinates dynamically.
- Forecast requests use the `America/Denver` timezone.
- Temperatures are requested in Fahrenheit.
- Precipitation is requested in inches.
- Forecast responses are cached for one hour, and the forecast client is configured to retry failed requests.

Open-Meteo provides the forecast and geocoding services used by this project. Review its terms and usage requirements before using the application in a commercial or high-traffic setting.

## Sprint Progress

### Sprint 1: Initial Dashboard

**Goal:** Build a working Python web application that retrieves forecast data and displays it in a browser.

- Integrated the Open-Meteo Forecast API.
- Processed daily forecast data.
- Created a FastAPI application served by Uvicorn.
- Rendered weather data with Jinja2 templates.
- Added static CSS and a health-check endpoint.
- Added response caching and retry handling.
- Practiced running the application on a Linux host.

### Sprint 2: City Search and Application Structure

**Goal:** Make the dashboard more useful and organize the code into clearer responsibilities.

- Added city search through a browser form.
- Integrated geocoding to translate city names into coordinates.
- Added readable weather descriptions from weather codes.
- Split page routes and API routes into separate modules.
- Moved weather fetching, geocoding, and formatting into a service module.
- Added a formatted weather API endpoint alongside the raw-data endpoint.
- Added handling for empty searches and locations with no results.

## Skills Practiced

This project provides hands-on practice with:

- Python application development
- REST-style API route design
- External API integration
- HTTP requests and JSON data
- Geocoding and coordinate-based queries
- Data transformation with Pandas
- Server-side HTML rendering with Jinja2
- Separating routes from service logic
- Caching and retry strategies
- Running a web application on a Linux host
- Documenting endpoints and local development setup

## Potential Future Improvements

Ideas for future sprints include:

- Display the resolved city and country in the dashboard.
- Improve date formatting and the overall forecast layout.
- Add clearer loading and error states for external API failures.
- Add automated tests for routes, geocoding, and weather-data formatting.
- Validate and normalize city-search input.
- Improve accessibility and responsive styling.
- Move configurable defaults, such as the default coordinates, into application settings.
- Add structured logging and more detailed health checks.
- Add containerization and a repeatable deployment workflow.

These are potential enhancements, not claims about features currently implemented.

## Resources

- [Project repository](https://github.com/S02441112/weather-dashboard)
- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [Uvicorn documentation](https://www.uvicorn.org/)
- [Open-Meteo Forecast API](https://open-meteo.com/en/docs)
- [Open-Meteo Geocoding API](https://open-meteo.com/en/docs/geocoding-api)
- [Pandas documentation](https://pandas.pydata.org/docs/)
- [Jinja documentation](https://jinja.palletsprojects.com/)
- [uv documentation](https://docs.astral.sh/uv/)

---

*This project is a work in progress and is being expanded through incremental development sprints.*
'''
