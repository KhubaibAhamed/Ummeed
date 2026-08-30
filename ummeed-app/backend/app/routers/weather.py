from fastapi import APIRouter, Depends

from app.dependencies import get_weather_provider
from app.models.schemas import WeatherResponse

router = APIRouter()


@router.get("/weather", response_model=WeatherResponse)
def get_weather(location: str, weather_provider=Depends(get_weather_provider)):
    return weather_provider.get_weather(location)
