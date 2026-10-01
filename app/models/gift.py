from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Gift(Base):
    __tablename__ = "gifts"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    wedding_id: Mapped[int] = mapped_column(
        ForeignKey("weddings.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    guest_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    gift: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    gift_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    amount: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )

    gift_date: Mapped[date] = mapped_column(
        Date,
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