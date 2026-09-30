# Weather Dashboard

A Python-based weather dashboard built as a programming practice project. The application retrieves weather forecast data from the Open-Meteo API, processes the response, and displays a seven-day forecast through a FastAPI web application.

This project is being developed incrementally through multiple sprints, with each sprint focused on practicing different programming, web development, API, and deployment concepts.

---

## Sprint 1: Initial Weather Dashboard

### Sprint Goal

Build a functional Python web application that can:

- Retrieve weather data from an external API
- Process and format API responses
- Serve the processed data through a web API
- Render weather data in an HTML webpage
- Provide a basic application health endpoint
- Run on a Linux server and accept connections from other devices

### Sprint Status

**Status:** Complete

### Sprint 1 Features

- Seven-day weather forecast
- Maximum daily temperature
- Minimum daily temperature
- Daily precipitation total
- Weather condition
- Open-Meteo API integration
- FastAPI web application
- Uvicorn ASGI server
- Jinja2 HTML templates
- Static CSS files
- API endpoint for weather data
- Health-check endpoint
- API response caching
- API request retry handling
- Linux server deployment

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| FastAPI | Web framework and API |
| Uvicorn | ASGI web server |
| Open-Meteo | Weather data API |
| Pandas | Weather data processing |
| Jinja2 | HTML templating |
| Requests Cache | API response caching |
| Retry Requests | API retry handling |
| HTML/CSS | Frontend presentation |
| `uv` | Python project/dependency management |

---

## Application Architecture

The application follows a simple request and data-processing flow:

```text
                    ┌─────────────────┐
                    │   Client/Web    │
                    │     Browser     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    FastAPI      │
                    │   Application   │
                    └────────┬────────┘
                             │
                 ┌───────────┴───────────┐
                 │                       │
                 ▼                       ▼
        ┌─────────────────┐    ┌─────────────────┐
        │ Weather Function│    │ Health Endpoint │
        └────────┬────────┘    └─────────────────┘
                 │
                 ▼
        ┌─────────────────┐
        │   Open-Meteo    │
        │      API        │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │ Process Weather │
        │      Data       │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │ Jinja2 Template │
        │   /index.html   │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │Weather Dashboard│
        └─────────────────┘
```
## Run program on server
- cd to ```~/Documents/Projects/weather-dashboard/app```
- run ```uv run uvicorn main:app --host 0.0.0.0 --port 8000```
- run locally ```uvicorn main:app --host 127.0.0.1 --port 8000```

## Directories
- Program implementation
  - ```/```
  - ```/api/weather```
  - ```/health```


- Management
  - ```/docs```
  - ```/redoc```

## Project Structure
```text
weather-dashboard/
│
├── app/
│   ├── main.py
│   │
│   ├── templates/
│   │   └── index.html
│   │
│   ├── static/
│   │   └── styles.css
│   │
│   └── .cache/
│
├── pyproject.toml
├── uv.lock
└── README.md

```
## Resources
- [Uvicorn](https://uvicorn.dev/)
- [FastAPI](https://fastapi.tiangolo.com/)
