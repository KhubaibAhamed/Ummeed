from app.services.live_data import fetch_live_data


class WorkingWeatherProvider:
    def get_weather(self, location):
        return {"humidity": 68, "temp_celsius": 28.5, "forecast_trend": "falling"}


class FailingWeatherProvider:
    def get_weather(self, location):
        raise TimeoutError("weather API timed out")


class WorkingMandiProvider:
    def get_price(self, crop, location):
        return {"price_per_quintal": 6850.0, "mandi_name": "Guntur", "date": "29/08/2026"}


class FailingMandiProvider:
    def get_price(self, crop, location):
        raise ValueError("no mandi price records found")


def test_fetches_weather_when_intent_needs_it_and_location_given():
    intent = {"needs_weather": True, "needs_mandi_price": False, "crop": None}

    result = fetch_live_data(
        intent, location="Guntur",
        weather_provider=WorkingWeatherProvider(), mandi_provider=WorkingMandiProvider(),
    )

    assert len(result) == 1
    assert result[0]["label"] == "Weather"
    assert "68" in result[0]["value"] or "falling" in result[0]["value"]


def test_fetches_mandi_price_when_intent_needs_it_with_crop_and_location():
    intent = {"needs_weather": False, "needs_mandi_price": True, "crop": "cotton"}

    result = fetch_live_data(
        intent, location="Guntur",
        weather_provider=WorkingWeatherProvider(), mandi_provider=WorkingMandiProvider(),
    )

    assert len(result) == 1
    assert result[0]["label"] == "Mandi price"
    assert "6850" in result[0]["value"]


def test_fetches_both_when_intent_needs_both():
    intent = {"needs_weather": True, "needs_mandi_price": True, "crop": "cotton"}

    result = fetch_live_data(
        intent, location="Guntur",
        weather_provider=WorkingWeatherProvider(), mandi_provider=WorkingMandiProvider(),
    )

    assert len(result) == 2


def test_skips_weather_gracefully_when_provider_fails():
    intent = {"needs_weather": True, "needs_mandi_price": False, "crop": None}

    result = fetch_live_data(
        intent, location="Guntur",
        weather_provider=FailingWeatherProvider(), mandi_provider=WorkingMandiProvider(),
    )

    assert result == []  # failure is swallowed, not raised — request still succeeds


def test_skips_mandi_gracefully_when_provider_fails_but_keeps_weather():
    intent = {"needs_weather": True, "needs_mandi_price": True, "crop": "cotton"}

    result = fetch_live_data(
        intent, location="Guntur",
        weather_provider=WorkingWeatherProvider(), mandi_provider=FailingMandiProvider(),
    )

    assert len(result) == 1
    assert result[0]["label"] == "Weather"


def test_skips_entirely_when_no_location_provided():
    intent = {"needs_weather": True, "needs_mandi_price": True, "crop": "cotton"}

    result = fetch_live_data(
        intent, location=None,
        weather_provider=WorkingWeatherProvider(), mandi_provider=WorkingMandiProvider(),
    )

    assert result == []  # can't fetch location-based data without a location


def test_returns_empty_when_intent_needs_nothing():
    intent = {"needs_weather": False, "needs_mandi_price": False, "crop": None}

    result = fetch_live_data(
        intent, location="Guntur",
        weather_provider=WorkingWeatherProvider(), mandi_provider=WorkingMandiProvider(),
    )

    assert result == []


def test_skips_mandi_when_needed_but_no_crop_detected():
    # can't look up a mandi price without knowing which crop
    intent = {"needs_weather": False, "needs_mandi_price": True, "crop": None}

    result = fetch_live_data(
        intent, location="Guntur",
        weather_provider=WorkingWeatherProvider(), mandi_provider=WorkingMandiProvider(),
    )

    assert result == []
