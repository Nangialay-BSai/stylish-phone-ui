"""init core tables

Revision ID: 0001_init_core
Revises: 
Create Date: 2025-08-24

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from geoalchemy2.types import Geography


# revision identifiers, used by Alembic.
revision: str = "0001_init_core"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Enums
    userrole = sa.Enum("Rider", "Driver", "Admin", name="userrole")
    userstatus = sa.Enum("active", "blocked", name="userstatus")
    walletstatus = sa.Enum("active", "frozen", name="walletstatus")
    wallettxtype = sa.Enum(
        "topup",
        "hold",
        "capture",
        "release",
        "payout",
        "refund",
        "transfer",
        name="wallettxtype",
    )
    wallettxstatus = sa.Enum("pending", "completed", "failed", name="wallettxstatus")
    ridestatus = sa.Enum(
        "requested",
        "offered",
        "accepted",
        "driver_arrived",
        "started",
        "completed",
        "cancelled",
        name="ridestatus",
    )

    userrole.create(op.get_bind(), checkfirst=True)
    userstatus.create(op.get_bind(), checkfirst=True)
    walletstatus.create(op.get_bind(), checkfirst=True)
    wallettxtype.create(op.get_bind(), checkfirst=True)
    wallettxstatus.create(op.get_bind(), checkfirst=True)
    ridestatus.create(op.get_bind(), checkfirst=True)

    # users
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("role", userrole, nullable=False),
        sa.Column("phone", sa.String(length=32), nullable=False, unique=True),
        sa.Column("name", sa.String(length=128), nullable=True),
        sa.Column("lang", sa.String(length=8), nullable=False, server_default="en"),
        sa.Column("status", userstatus, nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_users_phone", "users", ["phone"], unique=True)
    op.create_index("ix_users_id", "users", ["id"], unique=False)

    # wallets
    op.create_table(
        "wallets",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), index=True),
        sa.Column("balance_afn", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("status", walletstatus, nullable=False, server_default="active"),
        sa.Column("limits_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_wallets_user_id", "wallets", ["user_id"], unique=False)

    # wallet_txs
    op.create_table(
        "wallet_txs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("wallet_id", sa.Integer(), sa.ForeignKey("wallets.id", ondelete="CASCADE"), index=True),
        sa.Column("type", wallettxtype, nullable=False),
        sa.Column("amount_afn", sa.Integer(), nullable=False),
        sa.Column("status", wallettxstatus, nullable=False, server_default="pending"),
        sa.Column("ref_type", sa.String(), nullable=True),
        sa.Column("ref_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_wallet_txs_wallet_id", "wallet_txs", ["wallet_id"], unique=False)

    # price_rules
    op.create_table(
        "price_rules",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("city", sa.String(length=64), nullable=False),
        sa.Column("ride_class", sa.String(length=32), nullable=False),
        sa.Column("base", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("per_km", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("per_min", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("wait_per_min", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("min_fare", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("surge_zones", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )
    op.create_index("ix_price_rules_city", "price_rules", ["city"], unique=False)
    op.create_index("ix_price_rules_class", "price_rules", ["ride_class"], unique=False)

    # rides
    op.create_table(
        "rides",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("rider_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("driver_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("status", ridestatus, nullable=False, server_default="requested"),
        sa.Column("ride_class", sa.String(length=32), nullable=False, server_default="Sedan"),
        sa.Column("city", sa.String(length=64), nullable=False, server_default="Kabul"),
        sa.Column("pickup_point", Geography(geometry_type="POINT", srid=4326)),
        sa.Column("dropoff_point", Geography(geometry_type="POINT", srid=4326)),
        sa.Column("route_polyline", sa.Text(), nullable=True),
        sa.Column("est_distance_m", sa.Integer(), nullable=True),
        sa.Column("est_duration_s", sa.Integer(), nullable=True),
        sa.Column("est_price_afn", sa.Integer(), nullable=True),
        sa.Column("actual_price_afn", sa.Integer(), nullable=True),
        sa.Column("surge_factor", sa.Numeric(4, 2), nullable=True),
        sa.Column("payment_method", sa.String(length=16), nullable=True),
        sa.Column("wallet_tx_id", sa.Integer(), sa.ForeignKey("wallet_txs.id", ondelete="SET NULL"), nullable=True),
        sa.Column("start_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("end_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("cancel_reason", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )


def downgrade() -> None:
    op.drop_table("rides")
    op.drop_index("ix_price_rules_class", table_name="price_rules")
    op.drop_index("ix_price_rules_city", table_name="price_rules")
    op.drop_table("price_rules")
    op.drop_index("ix_wallet_txs_wallet_id", table_name="wallet_txs")
    op.drop_table("wallet_txs")
    op.drop_index("ix_wallets_user_id", table_name="wallets")
    op.drop_table("wallets")
    op.drop_index("ix_users_id", table_name="users")
    op.drop_index("ix_users_phone", table_name="users")
    op.drop_table("users")

    # Enums
    for enum_name in [
        "ridestatus",
        "wallettxstatus",
        "wallettxtype",
        "walletstatus",
        "userstatus",
        "userrole",
    ]:
        sa.Enum(name=enum_name).drop(op.get_bind(), checkfirst=True)
