from typing import Protocol

import httpx

# Humidity swing below this is treated as noise, not a real trend.
TREND_THRESHOLD = 5


class WeatherProvider(Protocol):
    """A Protocol so /query and /weather logic can be tested without a live API call."""

    def get_weather(self, location: str) -> dict: ...


def parse_openweather_response(current: dict, forecast: dict) -> dict:
    """
    Turns OpenWeatherMap's raw current + forecast JSON into our clean shape.
    forecast_trend is derived by comparing current humidity to the nearest forecast
    point — "will it get more or less humid soon" is what actually matters for a
    farmer deciding whether to spray, not the raw forecast numbers themselves.
    """
    humidity = current["main"]["humidity"]
    temp_celsius = current["main"]["temp"]

    forecast_points = forecast.get("list", [])
    if not forecast_points:
        trend = "stable"
    else:
        next_humidity = forecast_points[0]["main"]["humidity"]
        diff = next_humidity - humidity
        if diff > TREND_THRESHOLD:
            trend = "rising"
        elif diff < -TREND_THRESHOLD:
            trend = "falling"
        else:
            trend = "stable"

    return {"humidity": humidity, "temp_celsius": temp_celsius, "forecast_trend": trend}


class OpenWeatherMapProvider:
    """
    Real implementation. Only exercised once OPENWEATHER_API_KEY is configured —
    not used in unit tests, which test parse_openweather_response directly instead.
    """

    def __init__(self, api_key: str, timeout_seconds: float = 3.0):
        if not api_key:
            raise ValueError("OPENWEATHER_API_KEY is required")
        self._api_key = api_key
        self._timeout = timeout_seconds

    def get_weather(self, location: str) -> dict:
        base = "https://api.openweathermap.org/data/2.5"
        params_common = {"q": location, "appid": self._api_key, "units": "metric"}

        with httpx.Client(timeout=self._timeout) as client:
            current_resp = client.get(f"{base}/weather", params=params_common)
            current_resp.raise_for_status()

            forecast_resp = client.get(f"{base}/forecast", params=params_common)
            forecast_resp.raise_for_status()

        return parse_openweather_response(current_resp.json(), forecast_resp.json())
