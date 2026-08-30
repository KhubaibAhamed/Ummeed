from pydantic import BaseModel


class QueryRequest(BaseModel):
    text: str
    language: str = "en"
    location: str | None = None


class Citation(BaseModel):
    document_title: str
    snippet: str
    page_ref: str | None = None


class LiveDataItem(BaseModel):
    label: str
    value: str
    source: str


class QueryResponse(BaseModel):
    answer: str
    citations: list[Citation]
    live_data: list[LiveDataItem]
    response_time_ms: int
    grounded: bool  # False if we couldn't find a confident match and said so honestly


class TranscribeResponse(BaseModel):
    text: str
    detected_language: str


class WeatherResponse(BaseModel):
    humidity: float
    temp_celsius: float
    forecast_trend: str


class MandiPriceResponse(BaseModel):
    price_per_quintal: float
    mandi_name: str
    date: str
