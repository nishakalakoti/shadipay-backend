from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    wedding_id: Mapped[int] = mapped_column(
        ForeignKey(
            "weddings.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # =====================================================
    # LINK PAYMENT TO GIFT
    # =====================================================

    gift_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "gifts.id",
            ondelete="CASCADE",
        ),
        nullable=True,
        unique=True,
        index=True,
    )

    transaction_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
        index=True,
    )

    guest_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    amount: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    method: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="UPI",
        server_default="UPI",
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="Success",
        server_default="Success",
    )

    payment_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )