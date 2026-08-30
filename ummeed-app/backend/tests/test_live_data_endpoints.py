from fastapi.testclient import TestClient

from app.dependencies import get_mandi_provider, get_weather_provider
from app.main import app


class FakeWeatherProvider:
    def get_weather(self, location):
        return {"humidity": 68, "temp_celsius": 28.5, "forecast_trend": "falling"}


class FakeMandiProvider:
    def get_price(self, crop, location):
        return {"price_per_quintal": 6850.0, "mandi_name": "Guntur", "date": "29/08/2026"}


class FakeMandiProviderNoData:
    def get_price(self, crop, location):
        raise ValueError("no mandi price records found")


def test_weather_endpoint_returns_parsed_data():
    app.dependency_overrides[get_weather_provider] = lambda: FakeWeatherProvider()
    client = TestClient(app)

    response = client.get("/weather", params={"location": "Guntur"})
    app.dependency_overrides.clear()

    assert response.status_code == 200
    body = response.json()
    assert body["humidity"] == 68
    assert body["forecast_trend"] == "falling"


def test_mandi_price_endpoint_returns_parsed_data():
    app.dependency_overrides[get_mandi_provider] = lambda: FakeMandiProvider()
    client = TestClient(app)

    response = client.get("/mandi-price", params={"crop": "cotton", "location": "Guntur"})
    app.dependency_overrides.clear()

    assert response.status_code == 200
    body = response.json()
    assert body["price_per_quintal"] == 6850.0
    assert body["mandi_name"] == "Guntur"


def test_mandi_price_endpoint_returns_404_when_no_data_found():
    app.dependency_overrides[get_mandi_provider] = lambda: FakeMandiProviderNoData()
    client = TestClient(app)

    response = client.get("/mandi-price", params={"crop": "durian", "location": "Nowhere"})
    app.dependency_overrides.clear()

    assert response.status_code == 404
