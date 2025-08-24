from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..schemas.rides import QuoteRequest, QuoteResponse
from ..services.pricing import estimate_price


router = APIRouter(prefix="/rides", tags=["rides"])


@router.post("/quote", response_model=QuoteResponse)
async def quote(payload: QuoteRequest, db: Session = Depends(get_db)):
    # TODO: integrate OSRM for real distance/ETA; stub with straight-line approx
    from math import radians, cos, sin, asin, sqrt

    def haversine(lat1, lon1, lat2, lon2):
        R = 6371.0
        dlon = radians(lon2 - lon1)
        dlat = radians(lat2 - lat1)
        a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        return R * c

    distance_km = haversine(payload.pickup.lat, payload.pickup.lng, payload.dropoff.lat, payload.dropoff.lng)
    duration_min = max(5.0, distance_km / 20.0 * 60.0)  # 20km/h avg in-city baseline
    price = estimate_price(db, city="Kabul", ride_class=payload.ride_class, distance_km=distance_km, duration_min=duration_min)
    eta_minutes = max(3, int(min(15, duration_min)))
    return QuoteResponse(price=price, eta_minutes=eta_minutes, polyline=None)
