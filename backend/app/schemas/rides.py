from pydantic import BaseModel


class LatLng(BaseModel):
    lat: float
    lng: float


class QuoteRequest(BaseModel):
    pickup: LatLng
    dropoff: LatLng
    ride_class: str = "Sedan"


class QuoteResponse(BaseModel):
    price: int
    eta_minutes: int
    polyline: str | None = None
