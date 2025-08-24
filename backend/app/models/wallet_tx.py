from sqlalchemy import Integer, Enum, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
import enum

from ..core.database import Base


class WalletTxType(str, enum.Enum):
    topup = "topup"
    hold = "hold"
    capture = "capture"
    release = "release"
    payout = "payout"
    refund = "refund"
    transfer = "transfer"


class WalletTxStatus(str, enum.Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"


class WalletTx(Base):
    __tablename__ = "wallet_txs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    wallet_id: Mapped[int] = mapped_column(Integer, ForeignKey("wallets.id", ondelete="CASCADE"), index=True)
    type: Mapped[WalletTxType] = mapped_column(Enum(WalletTxType), nullable=False)
    amount_afn: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[WalletTxStatus] = mapped_column(Enum(WalletTxStatus), nullable=False, default=WalletTxStatus.pending)
    ref_type: Mapped[str | None] = mapped_column()
    ref_id: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(tz=timezone.utc), nullable=False)
