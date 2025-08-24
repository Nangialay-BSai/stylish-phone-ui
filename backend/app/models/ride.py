from sqlalchemy import Integer, Enum, DateTime, ForeignKey, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
import enum
from geoalchemy2 import Geography

from ..core.database import Base


class RideStatus(str, enum.Enum):
    requested = "requested"
    offered = "offered"
    accepted = "accepted"
    driver_arrived = "driver_arrived"
    started = "started"
    completed = "completed"
    cancelled = "cancelled"


class Ride(Base):
    __tablename__ = "rides"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rider_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="SET NULL"), index=True, nullable=True)
    driver_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="SET NULL"), index=True, nullable=True)
    status: Mapped[RideStatus] = mapped_column(Enum(RideStatus), nullable=False, default=RideStatus.requested)
    ride_class: Mapped[str] = mapped_column(String(32), nullable=False, default="Sedan")
    city: Mapped[str] = mapped_column(String(64), nullable=False, default="Kabul")
    pickup_point: Mapped[bytes] = mapped_column(Geography(geometry_type="POINT", srid=4326))
    dropoff_point: Mapped[bytes] = mapped_column(Geography(geometry_type="POINT", srid=4326))
    route_polyline: Mapped[str | None] = mapped_column(String, nullable=True)
    est_distance_m: Mapped[int | None] = mapped_column(Integer)
    est_duration_s: Mapped[int | None] = mapped_column(Integer)
    est_price_afn: Mapped[int | None] = mapped_column(Integer)
    actual_price_afn: Mapped[int | None] = mapped_column(Integer)
    surge_factor: Mapped[float | None] = mapped_column(Numeric(4, 2))
    payment_method: Mapped[str | None] = mapped_column(String(16))
    wallet_tx_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("wallet_txs.id", ondelete="SET NULL"))
    start_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    end_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    cancel_reason: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(tz=timezone.utc), nullable=False)
