import pytest
from app.services.weather import format_weather_data, validate_place, query_openmeteo


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


def test_query_openmeteo_with_mock(mocker):
    # fake API response object that matches the methods query_openmeteo uses
    mock_response = mocker.Mock()
    mock_response.Latitude.return_value = 39.7392
    mock_response.Longitude.return_value = -104.9903
    mock_response.Elevation.return_value = 1609.3
    mock_response.Timezone.return_value = b"America/Denver"     #b for bytes instead of string
    mock_response.TimezoneAbbreviation.return_value = b"MDT"
    mock_response.UTCOffsetSeconds.return_value = -21600

    mock_daily = mocker.Mock()
    mock_daily.Time.return_value = [1760505600]      # 2025-10-15 UTC timestamp
    mock_daily.TimeEnd.return_value = [1760592000]
    mock_daily.Interval.return_value = 86400

    max_var = mocker.Mock()
    max_var.ValuesAsNumpy.return_value = [47.8475799560547]
    min_var = mocker.Mock()
    min_var.ValuesAsNumpy.return_value = [37.5140151977539]
    precip_var = mocker.Mock()
    precip_var.ValuesAsNumpy.return_value = [5.6789]
    weather_code_var = mocker.Mock()
    weather_code_var.ValuesAsNumpy.return_value = [3]

    mock_daily.Variables.side_effect = [max_var, min_var, precip_var, weather_code_var]
    mock_response.Daily.return_value = mock_daily

    # patch the client created inside query_openmeteo
    mock_client = mocker.Mock()
    mock_client.weather_api.return_value = [mock_response]

    mocker.patch("app.services.weather.openmeteo_requests.Client", return_value=mock_client)
    # avoid real cache/retry setup
    mocker.patch("app.services.weather.requests_cache.CachedSession")
    mocker.patch("app.services.weather.retry")

    result = query_openmeteo(39.7392, -104.9903)

    assert result[0]["temperature_2m_max"] == 47.8475799560547
    assert result[0]["temperature_2m_min"] == 37.5140151977539
    assert result[0]["precipitation_sum"] == 5.6789
    assert result[0]["weather_code"] == 3