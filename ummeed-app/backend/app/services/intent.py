import re

WEATHER_KEYWORDS = {
    "rain", "weather", "humidity", "spray", "irrigate", "irrigation",
    "monsoon", "temperature", "dry", "wet", "forecast",
}

MANDI_KEYWORDS = {
    "sell", "price", "mandi", "market", "rate", "buy", "cost", "worth",
}

# Small, hand-curated list — enough for a hackathon demo corpus, not exhaustive.
# Extending this is a one-line change, deliberately kept simple over building real NER.
KNOWN_CROPS = {
    "cotton", "paddy", "rice", "wheat", "tomato", "chilli", "chili",
    "groundnut", "maize", "sugarcane", "onion", "banana",
}


def detect_intent(query: str) -> dict:
    """
    Decides whether a query needs live weather and/or mandi price data, and pulls
    out a known crop name if mentioned. Deliberately simple keyword matching —
    good enough to route live-data calls correctly for a curated demo corpus,
    not a production NLU system.

    Keyword matching uses substring containment (so "prices" still matches "price"),
    but crop extraction uses word-boundary regex — otherwise "price" would falsely
    match the crop "rice" as a substring.
    """
    lower_query = query.lower()

    needs_weather = any(kw in lower_query for kw in WEATHER_KEYWORDS)
    needs_mandi_price = any(kw in lower_query for kw in MANDI_KEYWORDS)

    crop = next(
        (c for c in KNOWN_CROPS if re.search(rf"\b{re.escape(c)}\b", lower_query)), None
    )

    return {
        "needs_weather": needs_weather,
        "needs_mandi_price": needs_mandi_price,
        "crop": crop,
    }
