from ..models.price_rule import PriceRule
from sqlalchemy.orm import Session


def estimate_price(
    db: Session,
    city: str,
    ride_class: str,
    distance_km: float,
    duration_min: float,
) -> int:
    rule = (
        db.query(PriceRule)
        .filter(PriceRule.city == city, PriceRule.ride_class == ride_class)
        .one_or_none()
    )
    if not rule:
        # basic defaults
        base = 30
        per_km = 12
        per_min = 2
        min_fare = 50
    else:
        base = rule.base
        per_km = rule.per_km
        per_min = rule.per_min
        min_fare = rule.min_fare

    price = int(base + per_km * distance_km + per_min * duration_min)
    return max(price, int(min_fare))
