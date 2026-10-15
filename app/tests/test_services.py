import pytest
from app.services.weather import format_weather_data, validate_place


def test_format_weather_data_converts_and_rounds_numbers():
    api_weather_data = [
        {
            "date": "2026-10-15T00:00:00-06:00",
            "temperature_2m_max": 47.8475799560547,
            "temperature_2m_min": 37.5140151977539,
            "precipitation_sum": 5.6789,
            "weather_code": 3
        }
    ]

    result = format_weather_data(api_weather_data)

    assert result == [
        {
            "day": "2026-10-15T00:00:00-06:00",
            "max_temp": 48,
            "min_temp": 38,
            "precipitation_sum": 5.68,
            "weather_code": "Overcast"
        },
    ]


@pytest.mark.parametrize(
    "value, expected",
    [
        (None, False),      # fails because place_name is None
        (123, False),       # fails because not isinstance(place_name, str)
        ("", False),        # fails because strip() == ""
        ("   ", False),     # fails because strip() == ""
        ("Denver", True),   # passes path through else
        ("  Colorado Springs  ", True),  # valid string with spaces around it
    ],
)
def test_validate_place(value, expected):
    assert validate_place(value) == expected

# def validate_place