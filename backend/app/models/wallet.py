from sqlalchemy import String, Integer, Numeric, Enum, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
import enum

from ..core.database import Base


class WalletStatus(str, enum.Enum):
    active = "active"
    frozen = "frozen"


class Wallet(Base):
    __tablename__ = "wallets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    balance_afn: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    status: Mapped[WalletStatus] = mapped_column(Enum(WalletStatus), nullable=False, default=WalletStatus.active)
    limits_json: Mapped[dict] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(tz=timezone.utc), nullable=False)
