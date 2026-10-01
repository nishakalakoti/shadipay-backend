from datetime import date, datetime

from sqlalchemy import Date, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Wedding(Base):
    __tablename__ = "weddings"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    firebase_uid: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True,
        index=True,
    )

    first_partner: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    second_partner: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    wedding_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    wedding_venue: Mapped[str] = mapped_column(
        String(255),
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