from sqlalchemy import Integer, String, Numeric, JSON
from sqlalchemy.orm import Mapped, mapped_column

from ..core.database import Base


class PriceRule(Base):
    __tablename__ = "price_rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    city: Mapped[str] = mapped_column(String(64), index=True)
    ride_class: Mapped[str] = mapped_column(String(32), index=True)
    base: Mapped[int] = mapped_column(Integer, default=0)
    per_km: Mapped[int] = mapped_column(Integer, default=0)
    per_min: Mapped[int] = mapped_column(Integer, default=0)
    wait_per_min: Mapped[int] = mapped_column(Integer, default=0)
    min_fare: Mapped[int] = mapped_column(Integer, default=0)
    surge_zones: Mapped[dict | None] = mapped_column(JSON, nullable=True)
