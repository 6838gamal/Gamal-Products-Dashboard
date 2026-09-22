"""موديل الأراضي والعقارات."""
from datetime import datetime, timezone
from sqlalchemy import String, Text, Integer, Boolean, Float, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.database.lands_base import LandsBase


class Land(LandsBase):
    __tablename__ = "lands"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    short_description: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    # بيانات عقارية
    land_type: Mapped[str | None] = mapped_column(String(50), nullable=True)   # أرض / شقة / فيلا / محل
    purpose: Mapped[str | None] = mapped_column(String(20), nullable=True)     # sale / rent
    price: Mapped[float] = mapped_column(Float, default=0)
    currency: Mapped[str] = mapped_column(String(10), default="SAR")
    area: Mapped[float | None] = mapped_column(Float, nullable=True)           # المساحة م²
    rooms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    bathrooms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    address: Mapped[str | None] = mapped_column(String(500), nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    district: Mapped[str | None] = mapped_column(String(100), nullable=True)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    features: Mapped[list] = mapped_column(JSON, default=list)                # مزايا
    images: Mapped[list] = mapped_column(JSON, default=list)                  # صور إضافية

    featured: Mapped[bool] = mapped_column(Boolean, default=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    cover_image: Mapped[str | None] = mapped_column(String(500), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
