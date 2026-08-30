from app.services.weather import parse_openweather_response

SAMPLE_CURRENT = {
    "main": {"temp": 28.5, "humidity": 68},
    "weather": [{"main": "Clouds", "description": "scattered clouds"}],
}


def test_parses_humidity_and_temperature():
    forecast = {"list": [{"main": {"humidity": 68}}]}
    result = parse_openweather_response(SAMPLE_CURRENT, forecast)

    assert result["humidity"] == 68
    assert result["temp_celsius"] == 28.5


def test_detects_falling_humidity_trend():
    forecast = {"list": [{"main": {"humidity": 55}}]}  # 13 points lower than current 68
    result = parse_openweather_response(SAMPLE_CURRENT, forecast)

    assert result["forecast_trend"] == "falling"


def test_detects_rising_humidity_trend():
    forecast = {"list": [{"main": {"humidity": 82}}]}  # 14 points higher than current 68
    result = parse_openweather_response(SAMPLE_CURRENT, forecast)

    assert result["forecast_trend"] == "rising"


def test_detects_stable_humidity_trend_within_threshold():
    forecast = {"list": [{"main": {"humidity": 70}}]}  # only 2 points different
    result = parse_openweather_response(SAMPLE_CURRENT, forecast)

    assert result["forecast_trend"] == "stable"


def test_missing_forecast_list_defaults_to_stable():
    result = parse_openweather_response(SAMPLE_CURRENT, {"list": []})
    assert result["forecast_trend"] == "stable"
