from sqlalchemy.orm import Session
from .core.database import SessionLocal
from .models.price_rule import PriceRule


def seed_price_rules(db: Session):
    defaults = [
        ("Kabul", "Moto", 20, 10, 1, 0, 30),
        ("Kabul", "Sedan", 30, 12, 2, 0, 50),
        ("Kabul", "XL", 40, 16, 3, 0, 80),
    ]
    for city, ride_class, base, per_km, per_min, wait_per_min, min_fare in defaults:
        exists = (
            db.query(PriceRule)
            .filter(PriceRule.city == city, PriceRule.ride_class == ride_class)
            .one_or_none()
        )
        if not exists:
            db.add(
                PriceRule(
                    city=city,
                    ride_class=ride_class,
                    base=base,
                    per_km=per_km,
                    per_min=per_min,
                    wait_per_min=wait_per_min,
                    min_fare=min_fare,
                )
            )
    db.commit()


def main():
    db = SessionLocal()
    try:
        seed_price_rules(db)
        print("Seeded price rules")
    finally:
        db.close()


if __name__ == "__main__":
    main()
