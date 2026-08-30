from typing import Protocol

import httpx


class MandiPriceProvider(Protocol):
    """A Protocol so /query and /mandi-price logic can be tested without a live API call."""

    def get_price(self, crop: str, location: str) -> dict: ...


def parse_agmarknet_response(raw: dict) -> dict:
    """
    Turns data.gov.in's Agmarknet raw JSON into our clean shape. Takes the first
    record — the API query itself filters by crop/market, so the first result is
    the most relevant real government-reported price, not an arbitrary pick.
    """
    records = raw.get("records", [])
    if not records:
        raise ValueError("no mandi price records found for this crop/location")

    record = records[0]
    return {
        "price_per_quintal": float(record["modal_price"]),
        "mandi_name": record["market"],
        "date": record["arrival_date"],
    }


class AgmarknetProvider:
    """
    Real implementation, wrapping data.gov.in's Agmarknet API. Only exercised once
    AGMARKNET_API_KEY is configured — not used in unit tests, which test
    parse_agmarknet_response directly instead.
    """

    BASE_URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"

    def __init__(self, api_key: str, timeout_seconds: float = 3.0):
        if not api_key:
            raise ValueError("AGMARKNET_API_KEY is required")
        self._api_key = api_key
        self._timeout = timeout_seconds

    def get_price(self, crop: str, location: str) -> dict:
        params = {
            "api-key": self._api_key,
            "format": "json",
            "filters[commodity]": crop,
            "filters[market]": location,
            "limit": 1,
        }

        with httpx.Client(timeout=self._timeout) as client:
            response = client.get(self.BASE_URL, params=params)
            response.raise_for_status()

        return parse_agmarknet_response(response.json())
