import logging

logger = logging.getLogger(__name__)


def fetch_live_data(
    intent: dict, location: str | None, weather_provider, mandi_provider
) -> list[dict]:
    """
    Fetches live weather/mandi data based on detected intent, with graceful
    degradation per the Phase 6 design: if a live API fails or times out, that
    item is silently dropped rather than failing the whole /query request — the
    farmer still gets their document-grounded answer, just without that extra data.

    Failures are logged (not raised) so this is debuggable without breaking the
    demo mid-presentation on a flaky venue connection.
    """
    if not location:
        return []

    live_data = []

    if intent.get("needs_weather"):
        try:
            weather = weather_provider.get_weather(location)
            live_data.append(
                {
                    "label": "Weather",
                    "value": f"{weather['humidity']}% humidity, {weather['forecast_trend']}",
                    "source": "OpenWeatherMap",
                }
            )
        except Exception:
            logger.warning("Weather fetch failed for location=%s, skipping.", location)

    if intent.get("needs_mandi_price") and intent.get("crop"):
        try:
            price = mandi_provider.get_price(intent["crop"], location)
            live_data.append(
                {
                    "label": "Mandi price",
                    "value": f"₹{price['price_per_quintal']:.0f}/quintal at {price['mandi_name']}",
                    "source": "Agmarknet (data.gov.in)",
                }
            )
        except Exception:
            logger.warning(
                "Mandi price fetch failed for crop=%s location=%s, skipping.",
                intent["crop"], location,
            )

    return live_data
